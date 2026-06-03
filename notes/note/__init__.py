from flask import Flask
from note.settings import config_map
from core.extensions import db, migrate, login_manager
from note.blueprints.auth import auth_bp
from note.blueprints.item import item_bp
from note.blueprints.profile import profile_bp
from note.blueprints.story import story_bp
from note.blueprints import admin_bp
from note.models import User

def create_app(config_name="dev"):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config_map[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(item_bp, url_prefix="/item")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(story_bp, url_prefix="/story")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.route("/")
    def index():
        from flask import render_template
        from note.models import Item
        # 取出所有状态为 available 的物品，按发布时间倒序排列
        items = Item.query.filter_by(status="available").order_by(Item.create_time.desc()).all()
        return render_template("index.html", items=items)
    return app