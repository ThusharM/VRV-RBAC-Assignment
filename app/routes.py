from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, login_required, logout_user
from app import db, bcrypt
from app.models import User
from app.forms import LoginForm, RegistrationForm

# Blueprint for authentication routes
auth = Blueprint("auth", __name__)

# Blueprint for main routes (dashboard, home, etc.)
main = Blueprint("main", __name__)

# Authentication Routes
@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Login successful!", "success")
            
            # Handle the 'next' parameter if it exists, otherwise redirect to dashboard
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("main.dashboard"))
        else:
            flash("Login unsuccessful. Please check email and password", "danger")
    return render_template("login.html", form=form)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if an Admin already exists
        existing_admin = User.query.filter_by(role="Admin").first()
        
        if form.role.data == "Admin" and existing_admin:
            # If an admin already exists, redirect to the admin dashboard for approval
            flash("An admin already exists. Your request for admin approval is pending.", "info")
            user = User(username=form.username.data, email=form.email.data, password=bcrypt.generate_password_hash(form.password.data).decode("utf-8"), role="Pending")
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.admin_dashboard'))  # Redirect to the admin dashboard for approval
        else:
            # Proceed with normal registration if no admin exists or role is User
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, role=form.role.data)
            db.session.add(user)
            db.session.commit()
            flash("Your account has been created! You can now log in.", "success")
            return redirect(url_for("auth.login"))
    
    return render_template("register.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))

# Main Routes
@main.route("/")
def home():
    """Home page route. Redirect authenticated users to the dashboard, others to the home page."""
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("home.html")

@main.route("/dashboard")
@login_required
def dashboard():
    """
    Dashboard page for authenticated users.
    """
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login", next=request.url))  # Pass the next URL parameter
    
    return render_template("dashboard.html")

# Admin Routes (Only accessible by Admin users)
@main.route("/admin_dashboard")
@login_required
def admin_dashboard():
    if current_user.role != 'Admin':
        flash("You do not have permission to access the Admin Dashboard.", "danger")
        return redirect(url_for("main.dashboard"))
    
    # Get users with Pending status
    pending_admin_requests = User.query.filter_by(role="Pending").all()
    
    return render_template("admin_dashboard.html", pending_admin_requests=pending_admin_requests)

@main.route("/approve_admin/<int:user_id>")
@login_required
def approve_admin(user_id):
    if current_user.role != 'Admin':
        flash("You do not have permission to approve users.", "danger")
        return redirect(url_for("main.dashboard"))
    
    user = User.query.get_or_404(user_id)
    user.role = 'Admin'  # Change the role to Admin
    db.session.commit()
    
    flash(f"User {user.username} has been approved as an Admin.", "success")
    return redirect(url_for("main.admin_dashboard"))

@main.route("/reject_admin/<int:user_id>")
@login_required
def reject_admin(user_id):
    if current_user.role != 'Admin':
        flash("You do not have permission to reject users.", "danger")
        return redirect(url_for("main.dashboard"))
    
    user = User.query.get_or_404(user_id)
    user.role = 'User'  # Revert the role to User if rejected
    db.session.commit()
    
    flash(f"User {user.username} has been rejected as an Admin.", "danger")
    return redirect(url_for("main.admin_dashboard"))

