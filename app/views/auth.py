from uuid import UUID
from app.models import User
from app import db, login_manager, bcrypt
from app.forms import LoginForm, RegisterForm
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user


bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


@login_manager.user_loader
def load_user(user_id: UUID):
    return User.query.get(user_id)

@bp_auth.route("/register", methods = ["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
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
        user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar_one()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for("root.main.index"))
        
        return redirect(url_for("root.auth.login"))
                
    
    return render_template(
        "views/auth/login.html",
        login_form = LoginForm()
    )