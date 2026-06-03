from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from core.extensions import db
from note.models import User, Item, Exchange, TimeCapsuleStory
from . import admin_bp
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, 'is_admin', False):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/")
@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    user_count = User.query.count()
    item_count = Item.query.count()
    exchange_count = Exchange.query.filter_by(status="completed").count()
    story_count = TimeCapsuleStory.query.count()
    
    # 按照物品模式统计
    modes = db.session.query(Item.mode, db.func.count(Item.id)).group_by(Item.mode).all()
    mode_stats = {m[0]: m[1] for m in modes}

    return render_template("dashboard.html", 
                           user_count=user_count, 
                           item_count=item_count, 
                           exchange_count=exchange_count, 
                           story_count=story_count,
                           mode_stats=mode_stats)

@admin_bp.route("/users")
@login_required
@admin_required
def users():
    q = request.args.get("q", "")
    if q:
        users_list = User.query.filter(
            (User.student_id.like(f"%{q}%")) | 
            (User.nickname.like(f"%{q}%")) | 
            (User.email.like(f"%{q}%"))
        ).all()
    else:
        users_list = User.query.all()
    return render_template("users.html", users=users_list, q=q)

@admin_bp.route("/users/delete/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("你不能删除你自己的管理员账号！")
        return redirect(url_for("admin.users"))
    
    # 删除该用户发布的所有物品及其交换申请
    for item in user.items:
        # 删除物品关联的所有申请
        Exchange.query.filter_by(item_id=item.id).delete()
        db.session.delete(item)
        
    # 删除该用户申请的所有交换
    Exchange.query.filter_by(applicant_id=user.id).delete()
    
    db.session.delete(user)
    db.session.commit()
    flash(f"已成功删除用户 {user.nickname}（学号：{user.student_id}）及其所有关联数据")
    return redirect(url_for("admin.users"))

@admin_bp.route("/items")
@login_required
@admin_required
def items():
    q = request.args.get("q", "")
    if q:
        items_list = Item.query.filter(
            (Item.title.like(f"%{q}%")) | 
            (Item.description.like(f"%{q}%"))
        ).all()
    else:
        items_list = Item.query.all()
    return render_template("items.html", items=items_list, q=q)

@admin_bp.route("/items/delete/<int:item_id>", methods=["POST"])
@login_required
@admin_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    # 删除物品关联的所有申请
    Exchange.query.filter_by(item_id=item.id).delete()
    db.session.delete(item)
    db.session.commit()
    flash(f"已强制下架并删除商品：{item.title}")
    return redirect(url_for("admin.items"))

@admin_bp.route("/stories")
@login_required
@admin_required
def stories():
    stories_list = TimeCapsuleStory.query.order_by(TimeCapsuleStory.create_time.desc()).all()
    return render_template("stories.html", stories=stories_list)

@admin_bp.route("/stories/delete/<int:story_id>", methods=["POST"])
@login_required
@admin_required
def delete_story(story_id):
    story = TimeCapsuleStory.query.get_or_404(story_id)
    db.session.delete(story)
    db.session.commit()
    flash("已成功隐藏/删除该胶囊故事")
    return redirect(url_for("admin.stories"))
