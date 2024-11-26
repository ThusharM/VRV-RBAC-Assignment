# Flask RBAC System with Admin Approval

This is a **Flask-based web application** that demonstrates a **Role-Based Access Control (RBAC)** system with **admin approval functionality**. The application allows users to register with either a **User** or **Admin** role. If an admin already exists, any user registering as an admin will be redirected to the admin dashboard for approval. The current admin can approve or reject pending admin requests.

## Features

- **Login and Registration**: Users can register and log in. Users can choose between a "User" or "Admin" role.
  
- **Admin Approval System**: If an admin already exists, users trying to register as "Admin" are redirected to the admin dashboard for approval. The current admin can approve or reject the request.

- **Admin Dashboard**: The current admin can manage pending admin requests, approving or rejecting them.

## Setup

### Requirements

- Python 3.x
- Flask
- Flask-Login
- Flask-WTF
- SQLAlchemy
- Flask-Bcrypt

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/ThusharM/VRV-RBAC-Assignment.git
   cd VRV-RBAC-Assignment
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**:

   Before running the application, you need to create a `.env` file to configure environment variables (e.g., secret keys, database URL).

   Here's an example `.env` file:

   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   SQLALCHEMY_DATABASE_URI=sqlite:///site.db
   SQLALCHEMY_TRACK_MODIFICATIONS=False
   ```

   Make sure to replace `your_secret_key_here` with a secure random string, and update `SQLALCHEMY_DATABASE_URI` with your preferred database URI (SQLite is used by default here).

5. **Set up the database**:

   Run the following commands to initialize the database and apply migrations:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Run the application**:

   Start the Flask application with:

   ```bash
   flask run
   ```

   The app will be available at `http://127.0.0.1:5000/`.

## Routes and Functionality

### Authentication Routes
- `/login`: User login page. If already logged in, redirects to the dashboard.
- `/register`: User registration page. Allows users to register as either "User" or "Admin". If an admin already exists, users trying to register as "Admin" are redirected to the admin dashboard for approval.
- `/logout`: Logs out the current user.

### Main Routes
- `/`: Home page. If logged in, redirects to the dashboard.
- `/dashboard`: User dashboard, displaying user information based on their role.
- `/admin_dashboard`: Admin dashboard (only accessible by the current admin) where pending admin requests can be approved or rejected.

### Admin Functions
- `/approve_admin/<int:user_id>`: Approve a pending admin request. The user’s role is updated to "Admin".
- `/reject_admin/<int:user_id>`: Reject a pending admin request. The user’s role is reverted to "User".

## Example Usage

1. **Register a User**:
   - Go to `/register`.
   - Choose a username, email, and "User" as the role.
   - Submit the registration form.

2. **Request Admin Privileges**:
   - Go to `/register`.
   - Choose a username, email, and "Admin" as the role.
   - If an admin already exists, you will be redirected to the admin dashboard for approval.

3. **Admin Approval**:
   - The admin can view pending admin requests at `/admin_dashboard`.
   - The admin can approve or reject the requests.
   
4. **Login**:
   - After approval, log in with your credentials.
   - Admins have access to the admin dashboard, while users have limited access to their own dashboards.

## Project Structure

```bash
flask-rbac-system/
│
├── app/
│   ├── __init__.py        # Flask app initialization
│   ├── routes.py          # All route handlers
│   ├── models.py          # Database models (User model)
│   ├── forms.py           # WTForms for login and registration
│   ├── templates/         # HTML templates
│   │   ├── base.html      # Base template
│   │   ├── home.html      # Home page template
│   │   ├── login.html     # Login page template
│   │   ├── register.html  # Registration page template
│   │   ├── dashboard.html # User dashboard template
│   │   └── admin_dashboard.html # Admin dashboard template
│           
│── config.py              # Configuration for Flask
├── requirements.txt       # Python dependencies
├── run.py                 # Entry point to run the application
├── .env                   # Environment variables configuration
└── README.md              # Project documentation

