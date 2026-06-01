from datetime import datetime
from flask_login import UserMixin
from core.extensions import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    nickname = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    contact_info = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_private = db.Column(db.Boolean, default=False)
    items = db.relationship("Item", backref="publisher", lazy=True)
    exchanges = db.relationship("Exchange", backref="applicant", lazy=True)
    # 注意：上面 backref="applicant"，不是 "user"

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    story = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    mode = db.Column(db.String(20), nullable=False)
    want_item = db.Column(db.String(100))
    borrow_days = db.Column(db.Integer)
    price = db.Column(db.Float)
    status = db.Column(db.String(20), default="available")
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    publisher_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # 关键：给 Item 加上 exchanges 关系
    exchanges = db.relationship("Exchange", backref="item", lazy=True)

class Exchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id"), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(20), default="pending")
    message = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    complete_time = db.Column(db.DateTime)

class TimeCapsuleStory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_image = db.Column(db.String(200), nullable=False)
    story_content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)