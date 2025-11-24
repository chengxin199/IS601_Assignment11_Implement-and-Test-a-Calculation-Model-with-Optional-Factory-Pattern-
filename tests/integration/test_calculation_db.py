# tests/integration/test_calculation_db.py
"""
Database Integration Tests for Calculation Models

These tests verify that the Calculation models work correctly with a real
PostgreSQL database. They test:
- Database insertion and retrieval
- Foreign key constraints
- Polymorphic queries
- Data integrity
- Error handling at the database level

These are TRUE integration tests that require a running PostgreSQL database.
"""

import pytest
import uuid
from sqlalchemy.exc import IntegrityError

from app.models.calculation import (
    Calculation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
)
from app.models.user import User


# ============================================================================
# Tests for Database Insertion and Retrieval
# ============================================================================

def test_insert_addition_calculation_to_db(db_session, test_user):
    """
    Test inserting an Addition calculation to the database.
    
    This verifies that:
    1. The factory pattern creates the correct subclass
    2. The calculation can be persisted to the database
    3. The calculation can be retrieved from the database
    4. The polymorphic type is correctly stored and retrieved
    """
    # Create calculation using factory
    calc = Calculation.create('addition', test_user.id, [10.5, 3, 2])
    
    # Add to database
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)
    
    # Verify it has an ID (was saved)
    assert calc.id is not None
    
    # Retrieve from database
    saved_calc = db_session.query(Calculation).filter_by(id=calc.id).first()
    
    # Verify it's still an Addition instance (polymorphism works)
    assert isinstance(saved_calc, Addition)
    assert saved_calc.type == 'addition'
    assert saved_calc.inputs == [10.5, 3, 2]
    assert saved_calc.user_id == test_user.id
    
    # Verify the result can be computed
    assert saved_calc.get_result() == 15.5


def test_insert_subtraction_calculation_to_db(db_session, test_user):
    """Test inserting a Subtraction calculation to the database."""
    calc = Calculation.create('subtraction', test_user.id, [20, 5, 3])
    db_session.add(calc)
    db_session.commit()
    
    saved_calc = db_session.query(Calculation).filter_by(id=calc.id).first()
    assert isinstance(saved_calc, Subtraction)
    assert saved_calc.get_result() == 12  # 20 - 5 - 3 = 12


def test_insert_multiplication_calculation_to_db(db_session, test_user):
    """Test inserting a Multiplication calculation to the database."""
    calc = Calculation.create('multiplication', test_user.id, [2, 3, 4])
    db_session.add(calc)
    db_session.commit()
    
    saved_calc = db_session.query(Calculation).filter_by(id=calc.id).first()
    assert isinstance(saved_calc, Multiplication)
    assert saved_calc.get_result() == 24


def test_insert_division_calculation_to_db(db_session, test_user):
    """Test inserting a Division calculation to the database."""
    calc = Calculation.create('division', test_user.id, [100, 2, 5])
    db_session.add(calc)
    db_session.commit()
    
    saved_calc = db_session.query(Calculation).filter_by(id=calc.id).first()
    assert isinstance(saved_calc, Division)
    assert saved_calc.get_result() == 10


def test_calculation_with_stored_result(db_session, test_user):
    """
    Test storing the result in the database.
    
    The result can be computed on-demand or stored. This tests
    the stored result scenario.
    """
    calc = Calculation.create('addition', test_user.id, [5, 10])
    
    # Compute and store the result
    calc.result = calc.get_result()
    
    db_session.add(calc)
    db_session.commit()
    
    # Retrieve and verify stored result
    saved_calc = db_session.query(Calculation).filter_by(id=calc.id).first()
    assert saved_calc.result == 15


# ============================================================================
# Tests for Foreign Key Constraints
# ============================================================================

def test_calculation_requires_valid_user_id(db_session):
    """
    Test that creating a calculation with invalid user_id fails.
    
    This verifies the foreign key constraint is enforced by the database.
    """
    # Create calculation with non-existent user_id
    fake_user_id = uuid.uuid4()
    calc = Calculation.create('addition', fake_user_id, [1, 2])
    
    db_session.add(calc)
    
    # Should raise IntegrityError due to foreign key constraint
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_cascade_delete_calculations_when_user_deleted(db_session):
    """
    Test that calculations are deleted when their user is deleted.
    
    This verifies the CASCADE delete constraint works correctly.
    """
    # Create user and calculations
    user = User(username="tempuser", email="temp@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    calc1 = Calculation.create('addition', user.id, [1, 2])
    calc2 = Calculation.create('multiplication', user.id, [3, 4])
    
    db_session.add_all([calc1, calc2])
    db_session.commit()
    
    # Verify calculations exist
    calc_count = db_session.query(Calculation).filter_by(
        user_id=user.id
    ).count()
    assert calc_count == 2
    
    # Delete user
    db_session.delete(user)
    db_session.commit()
    
    # Verify calculations were cascade deleted
    calc_count = db_session.query(Calculation).filter_by(
        user_id=user.id
    ).count()
    assert calc_count == 0


# ============================================================================
# Tests for Polymorphic Queries
# ============================================================================

def test_query_all_calculations_polymorphic(db_session, test_user):
    """
    Test querying all calculations returns correct polymorphic types.
    
    This demonstrates that SQLAlchemy's polymorphic inheritance works
    correctly with the database.
    """
    # Create different types of calculations
    calc1 = Calculation.create('addition', test_user.id, [1, 2])
    calc2 = Calculation.create('subtraction', test_user.id, [10, 3])
    calc3 = Calculation.create('multiplication', test_user.id, [2, 5])
    calc4 = Calculation.create('division', test_user.id, [100, 5])
    
    db_session.add_all([calc1, calc2, calc3, calc4])
    db_session.commit()
    
    # Query all calculations
    all_calcs = db_session.query(Calculation).all()
    
    # Verify we got all 4
    assert len(all_calcs) == 4
    
    # Verify each has the correct type
    types = [type(calc).__name__ for calc in all_calcs]
    assert 'Addition' in types
    assert 'Subtraction' in types
    assert 'Multiplication' in types
    assert 'Division' in types


def test_query_specific_calculation_type(db_session, test_user):
    """
    Test querying for a specific calculation type.
    
    You can filter by type to get only instances of that type.
    """
    # Create mixed types
    calc1 = Addition(user_id=test_user.id, inputs=[1, 2])
    calc2 = Addition(user_id=test_user.id, inputs=[3, 4])
    calc3 = Subtraction(user_id=test_user.id, inputs=[10, 5])
    
    db_session.add_all([calc1, calc2, calc3])
    db_session.commit()
    
    # Query only Addition calculations using filter on type
    additions = db_session.query(Calculation).filter_by(type='addition').all()
    
    assert len(additions) == 2
    assert all(isinstance(calc, Addition) for calc in additions)


def test_filter_calculations_by_type_string(db_session, test_user):
    """
    Test filtering calculations by the type discriminator column.
    """
    # Create mixed types
    calc1 = Calculation.create('multiplication', test_user.id, [2, 3])
    calc2 = Calculation.create('multiplication', test_user.id, [4, 5])
    calc3 = Calculation.create('division', test_user.id, [100, 2])
    
    db_session.add_all([calc1, calc2, calc3])
    db_session.commit()
    
    # Filter by type
    mult_calcs = db_session.query(Calculation).filter_by(
        type='multiplication'
    ).all()
    
    assert len(mult_calcs) == 2
    assert all(calc.type == 'multiplication' for calc in mult_calcs)


# ============================================================================
# Tests for User-Calculation Relationship
# ============================================================================

def test_user_calculations_relationship(db_session, test_user):
    """
    Test the bidirectional relationship between User and Calculation.
    
    This verifies that:
    1. We can access user.calculations
    2. We can access calculation.user
    3. The relationship is properly maintained
    """
    # Create calculations for the user
    calc1 = Calculation.create('addition', test_user.id, [1, 2])
    calc2 = Calculation.create('subtraction', test_user.id, [10, 5])
    
    db_session.add_all([calc1, calc2])
    db_session.commit()
    
    # Refresh to load relationships
    db_session.refresh(test_user)
    
    # Test user -> calculations relationship
    assert len(test_user.calculations) == 2
    assert calc1 in test_user.calculations
    assert calc2 in test_user.calculations
    
    # Test calculation -> user relationship
    db_session.refresh(calc1)
    assert calc1.user == test_user
    assert calc1.user.username == "testuser"


def test_multiple_users_with_calculations(db_session):
    """
    Test that multiple users can have their own calculations.
    
    This ensures calculations are properly isolated by user.
    """
    # Create two users
    user1 = User(username="user1", email="user1@example.com")
    user2 = User(username="user2", email="user2@example.com")
    
    db_session.add_all([user1, user2])
    db_session.commit()
    db_session.refresh(user1)
    db_session.refresh(user2)
    
    # Create calculations for each user
    calc1 = Calculation.create('addition', user1.id, [1, 2])
    calc2 = Calculation.create('multiplication', user1.id, [3, 4])
    calc3 = Calculation.create('division', user2.id, [100, 5])
    
    db_session.add_all([calc1, calc2, calc3])
    db_session.commit()
    
    # Verify each user has correct calculations
    db_session.refresh(user1)
    db_session.refresh(user2)
    
    assert len(user1.calculations) == 2
    assert len(user2.calculations) == 1
    
    # Verify calculations belong to correct users
    user1_calc_ids = [c.id for c in user1.calculations]
    assert calc1.id in user1_calc_ids
    assert calc2.id in user1_calc_ids
    assert calc3.id not in user1_calc_ids


# ============================================================================
# Tests for Data Integrity and Edge Cases
# ============================================================================

def test_calculation_timestamps_are_set(db_session, test_user):
    """
    Test that created_at and updated_at timestamps are automatically set.
    """
    calc = Calculation.create('addition', test_user.id, [1, 2])
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)
    
    assert calc.created_at is not None
    assert calc.updated_at is not None
    # Timestamps should be very close (within 1 second)
    time_diff = abs((calc.updated_at - calc.created_at).total_seconds())
    assert time_diff < 1.0


def test_calculation_with_large_inputs_list(db_session, test_user):
    """
    Test that calculations can handle large lists of inputs.
    
    JSON column should handle variable-length arrays efficiently.
    """
    large_inputs = list(range(1, 101))  # 100 numbers
    calc = Calculation.create('addition', test_user.id, large_inputs)
    
    db_session.add(calc)
    db_session.commit()
    db_session.refresh(calc)
    
    saved_calc = db_session.query(Calculation).filter_by(id=calc.id).first()
    assert len(saved_calc.inputs) == 100
    assert saved_calc.inputs == large_inputs


def test_calculation_with_negative_numbers(db_session, test_user):
    """
    Test that calculations work with negative numbers.
    """
    calc = Calculation.create('addition', test_user.id, [-5, -10, 3])
    db_session.add(calc)
    db_session.commit()
    
    saved_calc = db_session.query(Calculation).filter_by(id=calc.id).first()
    assert saved_calc.get_result() == -12


def test_calculation_with_decimal_precision(db_session, test_user):
    """
    Test that calculations maintain decimal precision.
    """
    calc = Calculation.create('division', test_user.id, [1.0, 3.0])
    db_session.add(calc)
    db_session.commit()
    
    saved_calc = db_session.query(Calculation).filter_by(id=calc.id).first()
    result = saved_calc.get_result()
    
    # Should be approximately 0.3333...
    assert abs(result - 0.33333333) < 0.00001


# ============================================================================
# Tests for Error Handling
# ============================================================================

def test_division_by_zero_after_db_retrieval(db_session, test_user):
    """
    Test that division by zero is caught even after database retrieval.
    
    This ensures validation works on both fresh objects and objects
    loaded from the database.
    """
    # Create calculation with zero (bypassing validation for testing)
    calc = Division(user_id=test_user.id, inputs=[100, 0])
    db_session.add(calc)
    db_session.commit()
    
    # Retrieve from database
    saved_calc = db_session.query(Division).filter_by(id=calc.id).first()
    
    # Should still raise error when computing result
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        saved_calc.get_result()


def test_invalid_inputs_type_in_database(db_session, test_user):
    """
    Test that invalid inputs type is caught when computing result.
    """
    # Create calculation with invalid inputs (bypassing validation)
    calc = Addition(user_id=test_user.id, inputs="not-a-list")
    db_session.add(calc)
    db_session.commit()
    
    saved_calc = db_session.query(Addition).filter_by(id=calc.id).first()
    
    with pytest.raises(ValueError, match="Inputs must be a list"):
        saved_calc.get_result()


# ============================================================================
# Tests for Complex Queries
# ============================================================================

def test_query_calculations_ordered_by_created_at(db_session, test_user):
    """
    Test querying calculations ordered by creation time.
    """
    import time
    
    calc1 = Calculation.create('addition', test_user.id, [1, 2])
    db_session.add(calc1)
    db_session.commit()
    
    time.sleep(0.01)  # Small delay to ensure different timestamps
    
    calc2 = Calculation.create('multiplication', test_user.id, [3, 4])
    db_session.add(calc2)
    db_session.commit()
    
    # Query ordered by created_at ascending
    calcs = db_session.query(Calculation).order_by(
        Calculation.created_at.asc()
    ).all()
    
    assert calcs[0].id == calc1.id
    assert calcs[1].id == calc2.id


def test_count_calculations_by_type(db_session, test_user):
    """
    Test counting calculations grouped by type.
    """
    # Create various calculations
    for _ in range(3):
        db_session.add(Calculation.create('addition', test_user.id, [1, 2]))
    for _ in range(2):
        db_session.add(Calculation.create('multiplication', test_user.id, [2, 3]))
    
    db_session.commit()
    
    # Count by type
    add_count = db_session.query(Calculation).filter_by(
        type='addition'
    ).count()
    mult_count = db_session.query(Calculation).filter_by(
        type='multiplication'
    ).count()
    
    assert add_count == 3
    assert mult_count == 2
