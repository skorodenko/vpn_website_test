from flask_login import logout_user
from flask import Blueprint, render_template, request, redirect, url_for


bp_main = Blueprint("main", __name__, url_prefix="")


@bp_main.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        logout_user()
        return redirect(url_for("root.main.index"))
    
    return render_template("views/index.html")