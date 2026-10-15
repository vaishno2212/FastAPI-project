# FastAPI Shipment & Authentication Training Project

This project is designed as a hands-on learning lab to take you from a complete beginner in Python backend development to building a production-ready REST API with authentication and database integration.

---

## What You Will Learn

This repository is split into three progressive learning stages:

1. **Stage 1: FastAPI Fundamentals (`main.py`)**
   - Understanding HTTP methods (`GET`, `POST`, `PUT`, `DELETE`).
   - Working with path parameters, query parameters, and request bodies.
   - In-memory data management and returning proper HTTP status codes.
   - Validating incoming requests with Pydantic schemas.

2. **Stage 2: Database Basics (`database.py` & `db.py`)**
   - Connecting to an SQLite database file without third-party dependencies.
   - Writing raw SQL: `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`.
   - Why parameterized queries (`?`) are critical to stop SQL Injection.
   - Encapsulating database logic inside reusable Python classes.

3. **Stage 3: Full Application with ORM & JWT Auth (`api.py`)**
   - Modern ORM modeling using **SQLModel** (built on SQLAlchemy + Pydantic).
   - Database session lifecycle and FastAPI dependency injection (`Depends`).
   - Secure password hashing using **Bcrypt** with salt generation.
   - Stateless authentication using **JSON Web Tokens (JWT)**.
   - Protecting private routes with Bearer token authorization.

---

## Project Structure

Here is how the project files fit together:

```text
├── main.py              # Stage 1: In-memory FastAPI starter code
├── database.py          # Stage 2: Standalone raw SQLite demonstration
├── db.py                # Stage 2: Database helper class for shipments
├── db_explained.md      # Detailed breakdown of database queries
├── api.py               # Stage 3: Full REST API with auth & shipments
├── auth.py              # JWT generation, token decoding, and auth dependency
├── hash.py              # Password hashing and verification using bcrypt
├── schemas.py           # Pydantic request & response validation models
├── database/
│   ├── models.py        # SQLModel table definitions (User, Shipment)
│   └── sessions.py      # Database engine & session generator (SQLite / PostgreSQL)
├── .env.example         # Example environment variables template
├── requirements.txt     # Python package dependencies (for pip)
├── pyproject.toml       # Project metadata (for pip or uv)
└── README.md            # You are here!
```

---

## Prerequisites

Before starting, make sure you have:

- **Python 3.10 or higher** installed on your system.  
  Verify in your terminal:
  ```bash
  python --version
  ```
- **Git** (optional, if cloning the repo).
- A code editor like **Visual Studio Code**.

---

## Step-by-Step Setup from Scratch

Follow these steps in order. Even if you have never used Python virtual environments before, this guide will get everything working.

### Step 1: Open Terminal in the Project Directory

Open VS Code, press ``Ctrl + ` `` (backtick) to open the integrated terminal, and ensure you are in the project folder.

---

### Step 2: Create a Virtual Environment

A virtual environment keeps the packages for this project isolated so they do not conflict with anything else on your computer.

#### Option A: Using Standard Python `venv` (Recommended for Beginners)
```bash
python -m venv .venv
```

#### Option B: Using `uv` (Fast alternative, if installed)
```bash
uv venv
```

You will see a `.venv` folder appear inside your project directory.

---

### Step 3: Activate the Virtual Environment

You must activate the virtual environment every time you open a new terminal to work on this project.

- **On Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  > **Note for Windows users:** If PowerShell gives an error saying *`Execution of scripts is disabled on this system`*, run this command once to allow the script for the current session:
  > ```powershell
  > Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  > .\.venv\Scripts\Activate.ps1
  > ```

- **On Windows (Command Prompt / CMD):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

- **On macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

When activated, you will see `(.venv)` at the beginning of your terminal prompt line.

---

### Step 4: Install Dependencies

With the virtual environment active, install all required packages:

#### Using `pip`:
```bash
pip install -r requirements.txt
```

#### Using `uv` (if you use uv):
```bash
uv pip install -r requirements.txt
# or
uv sync
```

---

### Step 5: Configure Environment Variables

1. Make a copy of `.env.example` and name it `.env`:
   - **On Windows (PowerShell):**
     ```powershell
     Copy-Item .env.example .env
     ```
   - **On Mac / Linux:**
     ```bash
     cp .env.example .env
     ```
2. Open `.env` in your editor. By default, it uses SQLite so you can test right away:
   ```env
   DATABASE_URL=sqlite:///database.db
   SECRET_KEY=super-secret-jwt-key-replace-in-production-123456
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
   *(No changes are needed to run locally with SQLite!)*

---

## Running the Code

### 1. Stage 1: In-Memory FastAPI App (`main.py`)

To practice the basics of FastAPI endpoints and schemas without worrying about databases:

```bash
uvicorn main:app --reload
```
or with FastAPI CLI:
```bash
fastapi dev main.py
```

- Open your browser at: `http://127.0.0.1:8000/docs`
- Press `Ctrl + C` in the terminal when you want to stop the server.

---

### 2. Stage 2: SQLite Scripts (`database.py` & `db.py`)

To understand how raw SQL queries and SQLite work in pure Python:

```bash
python database.py
```
You will see output in the terminal showing table creation, data insertion, and queries using `fetchall()` and `fetchone()`.

To test password hashing logic separately:
```bash
python hash.py
```

---

### 3. Stage 3: The Full Backend API (`api.py`)

This runs the main production-ready application with database integration, password hashing, and user authentication:

```bash
uvicorn api:app --reload
```
or:
```bash
fastapi dev api.py
```

- The API is live at: `http://127.0.0.1:8000`
- Interactive Swagger documentation: `http://127.0.0.1:8000/docs`
- Alternative ReDoc documentation: `http://127.0.0.1:8000/redoc`

---

## Testing the API Step-by-Step in Swagger UI

Open `http://127.0.0.1:8000/docs` in your browser. This gives you an interactive dashboard to test every single endpoint.

### Step 1: Register a New User
- Expand **`POST /create-user`**.
- Click **Try it out**.
- Enter JSON payload:
  ```json
  {
    "username": "student1",
    "email": "student1@example.com",
    "password": "mypassword123"
  }
  ```
- Click **Execute**. You should get a `201 Created` status with the user ID and username (the password is never returned).

---

### Step 2: Login and Get a JWT Token
- Expand **`POST /login`**.
- Click **Try it out**.
- Enter your login credentials:
  ```json
  {
    "email": "student1@example.com",
    "password": "mypassword123"
  }
  ```
- Click **Execute**. You will receive a response like:
  ```json
  {
    "message": "Login successful",
    "userid": 1,
    "username": "student1",
    "email": "student1@example.com",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
- Copy the string inside `"token"`.

---

### Step 3: Test the Protected Route (`/users/me`)
- Scroll to the top of the Swagger page and click the green **Authorize** button.
- Paste your copied token into the text box and click **Authorize**, then click **Close**.
- Now expand **`GET /users/me`**, click **Try it out**, and click **Execute**.
- The API decodes your token, identifies you, and returns your user details!

---

### Step 4: Test Logout & Token Invalidation
- While authorized, expand **`POST /logout`**.
- Click **Try it out**, then click **Execute**.
- You will receive `{"message": "Logged out successfully"}`.
- Now try executing **`GET /users/me`** again with that same token:
  - You will receive `401 Unauthorized` with detail: `"Token has been revoked, please log in again"`.
  - This demonstrates how stateless JWT tokens can be securely invalidated before their expiration using a database revocation list!

---

### Step 5: Manage Shipments (CRUD)
- **Create a shipment:**
  - Endpoint: `POST /new-shipment`
  - Sample Body:
    ```json
    {
      "weight": 8.5,
      "content": "Electronics and Monitor",
      "destination": "New York, NY",
      "expected_delivery": "2026-11-01T12:00:00",
      "status": "placed"
    }
    ```
- **View all shipments:**
  - Endpoint: `GET /shipments`
- **View single shipment:**
  - Endpoint: `GET /shipments/{shipment_id}` (e.g., id `1`)
- **Partially update a shipment:**
  - Endpoint: `PATCH /shipments/{shipment_id}` (e.g., update only `"status": "in_transit"`)
- **Delete a shipment:**
  - Endpoint: `DELETE /shipments/{shipment_id}`

---

## Switching to PostgreSQL (Optional)

By default, the project runs using a local SQLite database (`database.db`), which requires zero setup.

If you have PostgreSQL installed and want to use it instead:
1. Ensure your PostgreSQL server is running.
2. Open your `.env` file.
3. Update `DATABASE_URL` with your PostgreSQL username, password, host, port, and database name:
   ```env
   DATABASE_URL=postgresql://postgres:yourpassword@127.0.0.1:5432/postgres
   ```
4. Restart the server (`uvicorn api:app --reload`). SQLModel will automatically connect to Postgres and create the tables.

---

## Common Issues & Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **`Execution of scripts is disabled on this system`** | Windows PowerShell security policy prevents running `.ps1` activation script. | Run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` then activate again. |
| **`address already in use` (Port 8000 busy)** | Another process is already running on port 8000. | Start on a different port: `uvicorn api:app --reload --port 8001` |
| **`ModuleNotFoundError: No module named 'fastapi'`** | Virtual environment is not activated or packages were not installed in it. | Make sure `(.venv)` is visible in your terminal, then run `pip install -r requirements.txt`. |
| **`401 Unauthorized` on `/users/me`** | The JWT token was not provided, has expired (after 30 min), or has an invalid secret key. | Log in again via `POST /login` and paste the new token into the **Authorize** dialog. |
| **`sqlite3.OperationalError: table already exists`** | SQL table initialization conflict. | Delete `database.db` and re-run `api.py` to recreate clean tables. |

---

## Exercises for Students

To test and expand your understanding, try adding these features:
1. **Shipment Ownership:** Add a `user_id` foreign key column to the `Shipment` model in `database/models.py`, and modify `POST /new-shipment` in `api.py` so only logged-in users can create shipments linked to their account.
2. **Role-Based Access Control:** Add a `role` field (e.g. `"admin"` vs `"customer"`) on the `User` model, and restrict `DELETE /shipments/{shipment_id}` so only admin users can delete records.
3. **Password Validation:** In `schemas.py`, add custom Pydantic validators on `UserCreate.password` to enforce minimum length, digits, and special characters.

Happy Learning!
