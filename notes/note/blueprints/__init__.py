from flask import Blueprint

auth_bp = Blueprint("auth", __name__, template_folder="../../templates/auth")
item_bp = Blueprint("item", __name__, template_folder="../../templates")
profile_bp = Blueprint("profile", __name__, template_folder="../../templates")
story_bp = Blueprint("story", __name__, template_folder="../../templates")

from . import auth, item, profile, story