from uuid import UUID
from app.models import User
from app import db, login_manager, bcrypt
from app.forms import LoginForm, RegisterForm
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required


bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


@login_manager.user_loader
def load_user(user_id: UUID):
    return User.query.get(user_id)


@bp_auth.route("/register", methods = ["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():        
        hashed_password = bcrypt \
            .generate_password_hash(form.password.data) \
            .decode("utf-8")
            
        user = User(username = form.username.data,
                    password = hashed_password)        
        
        db.session.add(user)
        db.session.commit()        
        
        return redirect(url_for("root.auth.login"))
    
    return render_template(
        "views/auth/register.html",
        register_form = form
    )


@bp_auth.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for("root.main.index"))
        
        return redirect(url_for("root.auth.login"))
                
    
    return render_template(
        "views/auth/login.html",
        login_form = LoginForm()
    )

    
@bp_auth.route("/logout", methods = ["POST"])
@login_required
def logout():
    if request.method == "POST":
        logout_user()
        return redirect(url_for("root.main.index"))