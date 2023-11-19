import re
import cgi
import requests
from itertools import chain
from bs4 import BeautifulSoup
from app import db
from sqlalchemy import func
from urllib.parse import urlparse
from app.models import Website, UsageTrack
from app.forms import WebsitesAdd
from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, redirect, url_for, abort, Response


bp_main = Blueprint("main", __name__, url_prefix="")


@bp_main.route("/")
def index():
    return render_template("views/index.html")


@bp_main.route("/websites", methods = ["GET"])
@login_required
def websites():
    tdata = (
        Website.query.where(Website.user_id == current_user.id)
        .with_entities(Website.id, Website.name, Website.url)
        .all()
    )

    return render_template(
        "views/websites.html",
        active_page="websites",
        add_form=WebsitesAdd(),
        tdata=tdata,
    )


@bp_main.route("/websites/add", methods = ["POST"])
@login_required
def websites_add():
    form = WebsitesAdd(request.form)
    if form.validate():
        user = current_user
        website = Website(
            name=form.name.data,
            url=form.url.data
        )

        user.websites.append(website)
        db.session.commit()

    return redirect(url_for("root.main.websites"))


@bp_main.route("/dashboard", methods = ["GET"])
@login_required
def dashboard():
    tdata = db.session.execute(
                db.select(
                    Website.name.label("name"),
                    Website.url.label("url"),
                    func.count().label("rrcount"),
                    func.sum(UsageTrack.downloaded).label("downloaded"),
                    func.sum(UsageTrack.uploaded).label("uploaded"),
                ).join(
                    Website
                ).group_by(
                    Website.id
                )
                .filter(
                    Website.user_id == current_user.id
                )
            ).all()
    
    return render_template(
        "views/dashboard.html",
        active_page="dashboard",
        tdata=tdata
    )


@bp_main.route("/websites/delete/<uuid:id>", methods = ["POST"])
@login_required
def websites_delete(id):
    website = Website.query.get(id)

    db.session.delete(website)
    db.session.commit()

    return redirect(url_for("root.main.websites"))


@bp_main.route("/<path:url>", methods = ["GET", "POST", "PUT", "DELETE"])
@login_required
def vpn(url):
    # Get the target URL for the request
    target_url = urlparse(f"https://{url}")
    
    website = (
        Website.query
        .where(Website.user_id == current_user.id)
        .filter_by(url = target_url.netloc).first()
    )
    
    # Only added website can be routed through 'vpn'
    if not website:
        return abort(404)
    
    # Track data upload
    cl = int(request.headers.get("Content-Length", 0))
    track = UsageTrack(uploaded = cl, website = website)
    db.session.add(track)
    db.session.commit()
    
    # Forward the request to the target URL
    resp = requests.request(
        method=request.method,
        url=target_url.geturl(),
        data=request.get_data(),
    )
    
    # Track data download
    cl = int(resp.headers.get("Content-Length", 0))
    track = UsageTrack(downloaded = cl, website = website)
    db.session.add(track)
    db.session.commit()
    
    content_type = resp.headers.get("Content-Type")
    mimetype, _ = cgi.parse_header(content_type)
    
    match mimetype:
        
        case "text/html":
            soup = BeautifulSoup(resp.content, "html.parser")
            
            # Substituting host with proxified host 
            # E.g. 1) for google href="/assset/..." -> href="localhost/www.google.com/asset/..."
            # E.g. 2) for google href="asset/..." -> href="localhost/www.googel.com/asset/..."
            proxy_host_url = urlparse(f"{request.host_url}{target_url.netloc}")
            for tag in chain(soup.findAll("a"), soup.findAll("link")):
                if tag.get("href"):
                    # Add slash at beginning if it starts not with / or h(ttp).
                    tag["href"] = re.sub(r"^([^h/])", r"/\g<1>", tag["href"], 1)
                    tag["href"] = re.sub(r"^/", f"{proxy_host_url.geturl()}/", tag["href"], 1)
            for tag in chain(soup.findAll("img"), soup.findAll("script")):
                if tag.get("src"):
                    # Add slash at beginning if it starts not with / or h(ttp).
                    tag["src"] = re.sub(r"^([^h/])", r"/\g<1>", tag["src"], 1)
                    tag["src"] = re.sub(r"^/", f"{proxy_host_url.geturl()}/", tag["src"], 1)
            
            return Response(
                str(soup), 
                resp.status_code,
                content_type=content_type
            )
            
        case "application/javascript":
            soup = BeautifulSoup(resp.content, "lxml")
            
            return Response(
                str(soup), 
                resp.status_code,
                content_type=content_type
            )
            
        case _:
            return Response(
                resp.content,
                resp.status_code,
                content_type=content_type
            )
