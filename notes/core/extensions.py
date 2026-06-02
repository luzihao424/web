from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from supabase import create_client, Client
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://jtxqosthhrfwgiylluag.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_dDu6t59sn16N8HN6ny14NQ_9gkrLPkg")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)