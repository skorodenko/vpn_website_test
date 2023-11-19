from flask import Blueprint
from .auth import bp_auth
from .main import bp_main


bp_root = Blueprint("root", __name__, url_prefix="/")
bp_root.register_blueprint(bp_auth)
bp_root.register_blueprint(bp_main)