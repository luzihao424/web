import os
import uuid
from flask import render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
from core.extensions import db
from note.models import Item, Exchange, TimeCapsuleStory
from note.forms import ItemForm, ExchangeForm
from . import item_bp

@item_bp.route("/publish", methods=["GET","POST"])
@login_required
def publish():
    form = ItemForm()
    if form.validate_on_submit():
        mode = form.mode.data
        want_item = form.want_item.data
        borrow_days = form.borrow_days.data
        price = form.price.data
        
        # Backend verification
        if mode == '以物换物' and not want_item:
            flash("以物换物模式下，想换物品不能为空！")
            return render_template("publish.html", form=form)
        if mode == '免费借用' and (not borrow_days or borrow_days <= 0):
            flash("免费借用模式下，借用时长必须大于 0 天！")
            return render_template("publish.html", form=form)
        if mode == '正常买卖' and (not price or price <= 0):
            flash("正常买卖模式下，交易金额必须大于 0 元！")
            return render_template("publish.html", form=form)
            
        # Clean unrelated fields based on selected mode
        if mode != '以物换物':
            want_item = None
        if mode != '免费借用':
            borrow_days = None
        if mode != '正常买卖':
            price = None

        # Handle file upload
        image_file = form.image.data
        filename = secure_filename(image_file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Ensure upload folder exists
        upload_folder = os.path.join(current_app.static_folder, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save file to disk
        image_path = os.path.join(upload_folder, unique_filename)
        image_file.save(image_path)
        
        # Store relative url path
        image_url = f"/static/uploads/{unique_filename}"
        
        item = Item(
            title=form.title.data,
            description=form.description.data,
            story=form.story.data,
            image_url=image_url,
            mode=mode,
            want_item=want_item,
            borrow_days=borrow_days,
            price=price,
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
    # 自动生成交换日志前缀
    log_prefix = f"【时光胶囊日志】：{item.publisher.nickname} 与 {ex.applicant.nickname} 于 {datetime.utcnow().strftime('%Y-%m-%d')} 顺利完成了关于《{item.title}》的交换。\n\n"
    
    story = TimeCapsuleStory(
        item_image=item.image_url,
        story_content=log_prefix + item.story
    )
    db.session.add(story)
    db.session.commit()
    flash("交换完成，已存入时光胶囊！")
    return redirect(url_for("profile.index"))