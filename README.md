# Module 11: Calculation Model with Factory Pattern & Database Integration

 **Docker Hub**: [`chengxin199/is601_module11`](https://hub.docker.com/r/chengxin199/is601_module11)

[![CI/CD](https://github.com/chengxin199/IS601_Assignment11_Implement-and-Test-a-Calculation-Model-with-Optional-Factory-Pattern-/actions/workflows/test.yml/badge.svg)](https://github.com/chengxin199/IS601_Assignment11_Implement-and-Test-a-Calculation-Model-with-Optional-Factory-Pattern-/actions)
[![Coverage](https://img.shields.io/badge/coverage-93%25-brightgreen)]()
[![Tests](https://img.shields.io/badge/tests-91%20passed-success)]()
[![Docker](https://img.shields.io/badge/docker-chengxin199%2Fis601__module11-blue?logo=docker)](https://hub.docker.com/r/chengxin199/is601_module11)

## 🎯 Project Overview

A FastAPI-based calculator application demonstrating:
- **SQLAlchemy Polymorphic Models** - Single-table inheritance for calculations
- **Factory Pattern** - Dynamic calculation type instantiation
- **Pydantic Schemas** - Comprehensive data validation
- **Database Integration** - Full PostgreSQL integration with real tests
- **CI/CD Pipeline** - Automated testing, security scanning, and Docker deployment

### ✨ Key Features

- ✅ **Polymorphic Calculation Models** (Addition, Subtraction, Multiplication, Division)
- ✅ **Factory Method Pattern** for flexible calculation creation
- ✅ **Comprehensive Test Suite** (91 tests, 93% coverage)
- ✅ **TRUE Database Integration Tests** (20 tests with PostgreSQL)
- ✅ **Pydantic Validation** with business rules (no division by zero, min inputs, etc.)
- ✅ **Foreign Key Relationships** with CASCADE delete
- ✅ **GitHub Actions CI/CD** with PostgreSQL service
- ✅ **Docker Deployment** to Docker Hub

## 📊 Test Results

```
✅ 91 Total Tests Passing (100%)
├── 26 Unit Tests (operations logic)
├── 19 Polymorphic Model Tests (factory pattern, inheritance)
├── 23 Pydantic Schema Tests (validation)
├── 20 Database Integration Tests (PostgreSQL) ⭐ NEW
├── 5 FastAPI Integration Tests (API endpoints)
└── Coverage: 93%
```

## 🏗️ Architecture

### Database Models (SQLAlchemy)
- **Polymorphic Inheritance**: `Calculation` base class with `Addition`, `Subtraction`, `Multiplication`, `Division` subclasses
- **Factory Pattern**: `Calculation.create()` returns appropriate subclass
- **Foreign Keys**: User → Calculations (CASCADE delete)
- **Fields**: `id`, `user_id`, `type`, `inputs`, `result`, `created_at`, `updated_at`

### Pydantic Schemas
- `CalculationType` - Enum for valid types
- `CalculationCreate` - Input validation
- `CalculationResponse` - Output serialization
- **Validators**: Division by zero, minimum inputs, type normalization

### Design Patterns
1. **Factory Pattern** - `Calculation.create()`
2. **Polymorphic Inheritance** - SQLAlchemy single-table
3. **Template Method** - Abstract `get_result()` method
4. **Data Transfer Objects** - Pydantic schemas

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- PostgreSQL (via Docker)

### Setup & Run

```bash
# Clone repository
git clone https://github.com/chengxin199/IS601_Assignment11_Implement-and-Test-a-Calculation-Model-with-Optional-Factory-Pattern-.git
cd module11_is601

# Option 1: Run with Docker (Recommended)
docker pull chengxin199/is601_module11:latest
docker run -p 8000:8000 chengxin199/is601_module11:latest

# Option 2: Run locally
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL database
docker compose up -d db

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Start application
uvicorn main:app --reload
```

### Database Integration Tests

The project includes **20 comprehensive database tests** that use a real PostgreSQL database:

```bash
# Run only database integration tests
pytest tests/integration/test_calculation_db.py -v

# Tests cover:
# ✓ Database insertion and retrieval
# ✓ Foreign key constraints
# ✓ CASCADE delete operations
# ✓ Polymorphic queries
# ✓ User-calculation relationships
# ✓ Data integrity and edge cases
# ✓ Complex queries (ordering, filtering, counting)
```

## 📦 Docker Deployment

```bash
# Build and start all services
docker compose up -d

# Services:
# - web: FastAPI application (port 8000)
# - db: PostgreSQL database (port 5432)
# - pgadmin: Database admin (port 5050)
```

## 🧪 Testing Strategy

### Unit Tests (`tests/unit/`)
- Test individual operation functions
- No external dependencies
- Fast execution

### Integration Tests (`tests/integration/`)
- **Polymorphic Models** - Factory pattern, inheritance behavior
- **Pydantic Schemas** - Validation logic
- **Database Integration** ⭐ - Real PostgreSQL operations
- **FastAPI Endpoints** - API request/response

### CI/CD Pipeline
```yaml
✓ Python 3.10 environment
✓ PostgreSQL service container
✓ Automated test execution
✓ Security scanning (Trivy)
✓ Docker Hub deployment
```

---

# 📦 Project Setup

---

# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🐳 5. (Optional) Docker Setup

> Skip if Docker isn't used in this module.

## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

# 🚀 6. Running the Project

- **Without Docker**:

```bash
python main.py
```

(or update this if the main script is different.)

- **With Docker**:

```bash
docker run -it --rm <image-name>
```

---

# 📝 7. Submission Instructions

After finishing your work:

```bash
git add .
git commit -m "Complete Module X"
git push origin main
```

Then submit the GitHub repository link as instructed.

---

# 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

---

# 📋 Module 11 Specific Information

## 🔧 Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0 (with polymorphic inheritance)
- **Validation**: Pydantic v2
- **Testing**: pytest, pytest-cov
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions
- **Security**: Trivy vulnerability scanner

## 📁 Project Structure

```
module11_is601/
├── app/
│   ├── core/
│   │   ├── config.py              # Pydantic settings
│   │   └── __init__.py
│   ├── models/
│   │   ├── calculation.py         # Polymorphic models ⭐
│   │   ├── user.py                # User model
│   │   └── __init__.py
│   ├── schemas/
│   │   ├── calculation.py         # Pydantic schemas ⭐
│   │   └── __init__.py
│   ├── operations/
│   │   └── __init__.py            # Basic operations
│   └── database.py                # DB configuration
├── tests/
│   ├── unit/                      # Unit tests
│   ├── integration/
│   │   ├── test_calculation.py           # Polymorphic tests
│   │   ├── test_calculation_schema.py    # Validation tests
│   │   ├── test_calculation_db.py        # DB integration ⭐ NEW
│   │   └── test_fastapi_calculator.py    # API tests
│   ├── e2e/                       # End-to-end tests
│   └── conftest.py                # Shared fixtures ⭐
├── .github/workflows/
│   └── test.yml                   # CI/CD pipeline ⭐
├── docker-compose.yml             # Multi-container setup
├── Dockerfile                     # Application container
├── main.py                        # FastAPI application
├── requirements.txt               # Dependencies
└── README.md                      # This file

⭐ = Recently enhanced/added for Module 11
```

## 🎓 Learning Objectives Achieved

✅ **Define Calculation Model**
- SQLAlchemy models with `id`, `user_id`, `type`, `inputs`, `result`
- Valid foreign key relationships
- Result computed on-demand via `get_result()`

✅ **Create Pydantic Schemas**
- `CalculationCreate` receives `type`, `inputs`, `user_id`
- `CalculationResponse` returns all fields including computed result
- Validation: no division by zero, minimum 2 inputs, valid types

✅ **Incorporate Factory Pattern**
- `Calculation.create()` factory method
- Returns correct subclass based on type string
- Demonstrates design pattern in data layer

✅ **Write Unit + Integration Tests**
- **Unit Tests**: 26 tests for operation logic
- **Integration Tests**: 
  - 19 tests for polymorphic behavior
  - 23 tests for schema validation
  - **20 tests with real PostgreSQL database** ⭐
  - 5 tests for FastAPI endpoints

✅ **Maintain CI/CD**
- GitHub Actions workflow with PostgreSQL service
- Runs all tests on push/PR
- Security scanning with Trivy
- Automatic Docker Hub deployment on success

## 💡 Key Implementation Highlights

### 1. Polymorphic Inheritance
```python
# Single table, multiple types
calc = Calculation.create('addition', user_id, [1, 2, 3])
assert isinstance(calc, Addition)  # Returns specific subclass
assert calc.get_result() == 6       # Type-specific behavior
```

### 2. Database Integration Testing
```python
# Real PostgreSQL operations
def test_insert_calculation_to_db(db_session, test_user):
    calc = Calculation.create('addition', test_user.id, [10, 5])
    db_session.add(calc)
    db_session.commit()
    
    saved_calc = db_session.query(Calculation).first()
    assert saved_calc.get_result() == 15
```

### 3. Factory Pattern
```python
# Centralized creation logic
calculation_classes = {
    'addition': Addition,
    'subtraction': Subtraction,
    'multiplication': Multiplication,
    'division': Division,
}
return calculation_classes[type](user_id=user_id, inputs=inputs)
```

## 🐛 Troubleshooting

### PostgreSQL Connection Issues
```bash
# Check if database is running
docker ps | grep postgres

# View database logs
docker logs postgres_db

# Restart database
docker compose restart db
```

### Test Failures
```bash
# Run specific test file
pytest tests/integration/test_calculation_db.py -v

# Run with detailed output
pytest tests/ -vv --tb=long

# Skip database tests (if DB not available)
pytest tests/ --ignore=tests/integration/test_calculation_db.py
```

### Docker Issues
```bash
# Clean up old containers and volumes
docker compose down -v

# Rebuild images
docker compose build --no-cache

# Start fresh
docker compose up -d --force-recreate
```

## 📊 Coverage Report

Generate detailed coverage report:
```bash
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html  # View in browser
```

Current coverage: **93%**

## 🚢 Deployment

### Quick Start with Docker Hub

```bash
# Pull and run the latest image
docker pull chengxin199/is601_module11:latest
docker run -p 8000:8000 chengxin199/is601_module11:latest

# Or run a specific version
docker pull chengxin199/is601_module11:v1.0
docker run -p 8000:8000 chengxin199/is601_module11:v1.0

# Access the application
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Local Development with Docker Compose

```bash
# Start all services
docker compose up -d

# Services:
# - web: FastAPI application (port 8000)
# - db: PostgreSQL database (port 5432)
# - pgadmin: Database admin (port 5050)

# View logs
docker compose logs -f web

# Stop all services
docker compose down
```

### Build and Push Your Own Image

```bash
# Build image
docker build -t chengxin199/is601_module11:latest .

# Tag with version
docker tag chengxin199/is601_module11:latest chengxin199/is601_module11:v1.0

# Push to Docker Hub
docker push chengxin199/is601_module11:latest
docker push chengxin199/is601_module11:v1.0
```

## 📝 Assignment Completion Checklist

- [x] SQLAlchemy Calculation model with all required fields
- [x] Valid foreign key to User model
- [x] Pydantic schemas with comprehensive validation
- [x] Factory pattern implementation
- [x] Unit tests for all operation types
- [x] Integration tests with real PostgreSQL database
- [x] Error handling (division by zero, invalid inputs)
- [x] CI/CD pipeline with PostgreSQL service
- [x] Docker deployment to Docker Hub
- [x] Documentation and README
- [x] 93% code coverage

---

# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is required for database integration tests.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)

---

## 👤 Author

**chengxin199**
- GitHub: [@chengxin199](https://github.com/chengxin199)
- Repository: [IS601_Assignment11](https://github.com/chengxin199/IS601_Assignment11_Implement-and-Test-a-Calculation-Model-with-Optional-Factory-Pattern-)

## 📄 License

This project is part of IS601 coursework.
