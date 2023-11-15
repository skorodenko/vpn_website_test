from app import db
from app.models import Website
from app.forms import WebsitesAdd
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, redirect, url_for


bp_main = Blueprint("main", __name__, url_prefix="")


@bp_main.route("/")
def index():
    return render_template("views/index.html")


@bp_main.route("/websites", methods = ["GET"])
@login_required
def websites():
    tdata = Website.query \
        .where(Website.user_id == current_user.id) \
        .with_entities(Website.id, Website.url).all()
    
    return render_template(
        "views/websites.html",
        active_page = "websites",
        add_form = WebsitesAdd(),
        tdata = tdata,
    )
    

@bp_main.route("/websites/add", methods = ["POST"])
@login_required
def websites_add():
    form = WebsitesAdd(request.form)
    if form.validate():
        user = current_user
        website = Website(url = form.url.data)
        
        user.websites.append(website)
        db.session.commit()
        
    return redirect(url_for("root.main.websites"))     
    

@bp_main.route("/websites/delete/<uuid:id>", methods = ["POST"])
@login_required
def websites_delete(id):
    website = Website.query.get(id)
    
    db.session.delete(website)
    db.session.commit()

    return redirect(url_for("root.main.websites"))