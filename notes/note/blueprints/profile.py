from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from core.extensions import db
from note.models import Item, Exchange
from . import profile_bp

@profile_bp.route("/")
@login_required
def index():
    # 预加载每个物品的 exchanges 关联数据
    my_items = Item.query.filter_by(publisher_id=current_user.id).options(
        db.joinedload(Item.exchanges)
    ).all()
    my_applies = Exchange.query.filter_by(applicant_id=current_user.id).all()
    return render_template("profile.html", items=my_items, applies=my_applies)
@profile_bp.route("/toggle-private")
@login_required
def toggle_private():
    current_user.is_private = not current_user.is_private
    db.session.commit()
    flash("隐私设置已更新")
    return redirect(url_for("profile.index"))