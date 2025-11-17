# Python Flask Project

User management API with role-based access control and compliance reporting.

### Implemented Features

1. GitHub Actions CI/CD - Automated linting and testing on every push and pull request
2. Active Users Management - Users can be marked as active/inactive with timestamp tracking
3. Access Reporting - Generate compliance reports showing users and their assigned roles
4. Role Entity Model - Many-to-many relationship between users and roles with unique constraints
5. Secrets Management - Environment-based configuration using `.env` files

### Further Development (I may develop these prior to Final Interview)

- Fix further security issues (such as passwords being in plain text)
- Demonstrate debugging practices and IDE integration
- PostGres migration would be also ideal

## Getting Started

**Prerequisites**

- Python 3.12+
- Poetry for dependency management

**Installation**

1. Clone the repository
   ```powershell
   git clone https://github.com/StevenSchmidtAusTex/project-python-flask.git
   cd project-python-flask
   ```

2. Install dependencies
   ```powershell
   poetry install
   ```

3. Set up environment variables
   
   Copy the .env file and generate a secret key:
   ```powershell
   Copy-Item .env.example .env
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   
   Update `.env` with generated secret key:
   ```
   SECRET_KEY=your-generated-secret-key-here
   DATABASE_URI=sqlite:///users.db
   FLASK_ENV=development
   ```

4. Initialize the database
   ```powershell
   poetry run flask db upgrade
   ```

5. Start the dev server
   ```powershell
   $env:FLASK_ENV="development"
   poetry run python app.py
   ```

   The API will be available at `http://127.0.0.1:5000`

## Using the API

**Register a New User**

Note: New users are created as inactive by default and must be activated before login.

```powershell
curl -X POST http://127.0.0.1:5000/register `
  -H "Content-Type: application/json" `
  -d '{"username":"Dev Userson", "email":"dev.userson@example.com", "password":"sosecure"}'
```

**Activate/Deactivate a User**

```powershell
# Toggle user active status (replace 1 with actual user_id)
curl -X PATCH http://127.0.0.1:5000/users/1/toggle-active
```

**Login**

```powershell
curl -X POST http://127.0.0.1:5000/login `
  -H "Content-Type: application/json" `
  -d '{"email":"dev.userson@example.com", "password":"sosecure"}'
```

Response for inactive user: `403 Forbidden`

**User Access Report (Compliance)**

```powershell
# All users
curl http://127.0.0.1:5000/users/report

# Active users only
curl http://127.0.0.1:5000/users/report?status=active

# Inactive users only
curl http://127.0.0.1:5000/users/report?status=inactive
```

**Create a Role**

```powershell
curl -X POST http://127.0.0.1:5000/roles `
  -H "Content-Type: application/json" `
  -d '{"role_name":"Developer", "department_name":"Engineering"}'
```

Note: The combination of `role_name` and `department_name` must be unique.

**List All Roles**

```powershell
curl http://127.0.0.1:5000/roles
```

**Assign a Role to a User**

```powershell
curl -X POST http://127.0.0.1:5000/users/1/roles `
  -H "Content-Type: application/json" `
  -d '{"role_id":1}'
```

**Get Roles for a User**

```powershell
curl http://127.0.0.1:5000/users/1/roles
```

**Remove a Role from a User**

```powershell
curl -X DELETE http://127.0.0.1:5000/users/1/roles/1
```

## Development

**Linting**

Install and run pre-commit hooks:
```powershell
pre-commit install
pre-commit run --all-files
```

**Testing**

Run the test suite:
```powershell
poetry run pytest --verbose
```

Tests cover:
- User registration and authentication
- Active/inactive user management
- Login restrictions for inactive users
- Role creation and assignment
- Compliance reporting
- Error handling

**CI/CD Pipeline**

GitHub Actions runs linting and tests on every push and pull request. See `.github/workflows/ci.yml` for configuration.

## Database Schema

**User Model**
- `id` - Primary Key
- `username` - Unique, Not Null
- `email` - Unique, Not Null
- `password` - Not Null (stored in plain text - known security issue)
- `inactive_since` - DateTime, Nullable (tracks when user was deactivated)
- Many-to-Many relationship with `Role`

**Role Model**
- `role_id` - Primary Key
- `role_name` - Not Null
- `department_name` - Not Null
- Unique Constraint: (`role_name`, `department_name`)
- Many-to-Many relationship with `User`

**Environment Configuration**

- Environment Variables: Sensitive config stored in `.env` files (not in source control)
- Config Validation: Production requires SECRET_KEY to be set

## Database Migrations

```powershell
# Create a new migration
poetry run flask db migrate -m "Description of changes"

# Apply migrations
poetry run flask db upgrade

# Rollback migrations
poetry run flask db downgrade
```

## Troubleshooting

**Issue**: User cannot log in after registration
- Solution: Activate the user first: `curl -X PATCH http://127.0.0.1:5000/users/{user_id}/toggle-active`

**Issue**: "SECRET_KEY environment variable is required"
- Solution: Generate a key with `python -c "import secrets; print(secrets.token_hex(32))"` and add to `.env`

## Implementation Notes

**Testing Approach**

I used quite a few more test fixtures and helper functions in `test_roles.py` compared to the simpler approach in `test_auth.py`. The role tests needed to set up users, roles, and assignments repeatedly, so I created fixtures to avoid duplication. It made the tests more readable - instead of 20 lines of setup per test, I could just use the fixture and focus on what was actually being tested.

**Service Layer Pattern**

The original repo had a `user_service.py` file, so when I added role management I created a matching `role_service.py` to stay consistent. This kept the route files relatively clean. They just handle request/response while the services do the actual database work.

The biggest positive impact here was testing. It's significantly easier to test a function like `assign_role_to_user()` directly than to mock out Flask request objects. Plus if I ever need to call these functions from somewhere else, I wouldn't have to go through the route handlers.

## Repository

https://github.com/StevenSchmidtAusTex/project-python-flask
