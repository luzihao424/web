from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from core.extensions import db
from note.models import Item, Exchange, TimeCapsuleStory
from note.forms import ItemForm, ExchangeForm
from . import item_bp

@item_bp.route("/publish", methods=["GET","POST"])
@login_required
def publish():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(
            title=form.title.data,
            description=form.description.data,
            story=form.story.data,
            image_url=form.image_url.data,
            mode=form.mode.data,
            want_item=form.want_item.data,
            borrow_days=form.borrow_days.data,
            publisher_id=current_user.id
        )
        db.session.add(item)
        db.session.commit()
        flash("发布成功！")
        return redirect(url_for("index"))
    return render_template("publish.html", form=form)

@item_bp.route("/<int:item_id>")
def detail(item_id):
    item = Item.query.get_or_404(item_id)
    form = ExchangeForm()
    return render_template("detail.html", item=item, form=form)

@item_bp.route("/exchange/<int:item_id>", methods=["POST"])
@login_required
def exchange(item_id):
    item = Item.query.get_or_404(item_id)
    if item.status != "available":
        flash("物品不可申请")
        return redirect(url_for("item.detail", item_id=item_id))
    if item.publisher_id == current_user.id:
        flash("不能申请自己的物品")
        return redirect(url_for("item.detail", item_id=item_id))
    form = ExchangeForm()
    if form.validate_on_submit():
        ex = Exchange(
            item_id=item_id,
            applicant_id=current_user.id,
            message=form.message.data
        )
        db.session.add(ex)
        db.session.commit()
        flash("申请已提交")
    return redirect(url_for("item.detail", item_id=item_id))

@item_bp.route("/approve/<int:ex_id>")
@login_required
def approve(ex_id):
    ex = Exchange.query.get_or_404(ex_id)
    item = Item.query.get_or_404(ex.item_id)
    if item.publisher_id != current_user.id:
        flash("无权限")
        return redirect(url_for("index"))
    ex.status = "approved"
    item.status = "exchanged"
    db.session.commit()
    flash("已同意交换")
    return redirect(url_for("profile.index"))

@item_bp.route("/complete/<int:ex_id>")
@login_required
def complete(ex_id):
    ex = Exchange.query.get_or_404(ex_id)
    if ex.applicant_id != current_user.id:
        flash("无权限")
        return redirect(url_for("index"))
    ex.status = "completed"
    ex.complete_time = datetime.utcnow()
    item = Item.query.get_or_404(ex.item_id)
    story = TimeCapsuleStory(
        item_image=item.image_url,
        story_content=item.story
    )
    db.session.add(story)
    db.session.commit()
    flash("交换完成，已存入时光胶囊！")
    return redirect(url_for("profile.index"))