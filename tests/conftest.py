# tests/conftest.py
"""
Shared test fixtures for unit, integration, and E2E tests.

This module provides fixtures for:
- Database testing with PostgreSQL
- FastAPI server for E2E tests
- Playwright browser automation
"""

import os
import subprocess
import time
import pytest
from playwright.sync_api import sync_playwright
import requests
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.user import User
from app.models.calculation import Calculation


# ============================================================================
# Database Fixtures for Integration Tests
# ============================================================================

@pytest.fixture(scope="session")
def test_database_url():
    """
    Get the test database URL from environment or use default.
    
    In CI/CD, this will be set to the PostgreSQL service URL.
    For local testing, you can override with environment variable.
    """
    return os.getenv(
        "TEST_DATABASE_URL",
        "postgresql://user:password@localhost:5432/myappdb"
    )


@pytest.fixture(scope="session")
def engine(test_database_url):
    """
    Create a SQLAlchemy engine for testing.
    
    This engine connects to a real PostgreSQL database and is used
    for all database integration tests.
    """
    engine = create_engine(test_database_url)
    
    # Create all tables before tests
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Drop all tables after all tests complete
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine):
    """
    Create a new database session for each test function.
    
    This fixture provides a clean database session for each test.
    All changes are committed during the test, and tables are
    cleaned up after the test completes.
    
    Usage:
        def test_something(db_session):
            user = User(username="test", email="test@example.com")
            db_session.add(user)
            db_session.commit()
            assert user.id is not None
    """
    # Create a new session for the test
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    # Clean up: rollback any uncommitted changes and close session
    session.rollback()
    session.close()
    
    # Clean all tables for next test
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
        session.commit()


@pytest.fixture(scope="function")
def test_user(db_session):
    """
    Create a test user in the database.
    
    This fixture provides a user that can be used in tests that
    require a valid user_id foreign key.
    
    Returns:
        User: A User instance that has been committed to the database
    """
    user = User(
        username="testuser",
        email="testuser@example.com"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# ============================================================================
# E2E Testing Fixtures
# ============================================================================

@pytest.fixture(scope='session')
def fastapi_server():
    """
    Fixture to start the FastAPI server before E2E tests and stop it after tests complete.
    """
    # Start FastAPI app
    fastapi_process = subprocess.Popen(['python', 'main.py'])
    
    # Define the URL to check if the server is up
    server_url = 'http://127.0.0.1:8000/'
    
    # Wait for the server to start by polling the root endpoint
    timeout = 30  # seconds
    start_time = time.time()
    server_up = False
    
    print("Starting FastAPI server...")
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(server_url)
            if response.status_code == 200:
                server_up = True
                print("FastAPI server is up and running.")
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    
    if not server_up:
        fastapi_process.terminate()
        raise RuntimeError("FastAPI server failed to start within timeout period.")
    
    yield
    
    # Terminate FastAPI server
    print("Shutting down FastAPI server...")
    fastapi_process.terminate()
    fastapi_process.wait()
    print("FastAPI server has been terminated.")


@pytest.fixture(scope="session")
def playwright_instance_fixture():
    """
    Fixture to manage Playwright's lifecycle.
    """
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance_fixture):
    """
    Fixture to launch a browser instance.
    """
    browser = playwright_instance_fixture.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """
    Fixture to create a new page for each test.
    """
    page = browser.new_page()
    yield page
    page.close()
