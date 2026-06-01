import random
import time
from flask import render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash
from core.extensions import db
from core.email import send_verification_email_async
from note.models import User
from note.forms import RegisterForm, LoginForm
from . import auth_bp

@auth_bp.route("/send-code", methods=["POST"])
def send_code():
    data = request.get_json() or {}
    email = data.get("email")
    action = data.get("action")
    if not email:
        return jsonify({"success": False, "message": "邮箱地址不能为空！"}), 400
        
    user = User.query.filter_by(email=email).first()
    if action == "register" and user:
        return jsonify({"success": False, "message": "该邮箱已注册，请直接登录！"}), 400
    elif action == "login" and not user:
        return jsonify({"success": False, "message": "该邮箱未注册，请先注册！"}), 400
        
    # Generate 6-digit random code
    code = f"{random.randint(100000, 999999)}"
    session["verify_code"] = code
    session["verify_email"] = email
    session["code_time"] = time.time()
    
    send_verification_email_async(email, code)
    return jsonify({"success": True, "message": "验证码发送成功，请注意查收！"})

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        code = form.code.data
        
        # Verify code in session
        cached_code = session.get("verify_code")
        cached_email = session.get("verify_email")
        cached_time = session.get("code_time", 0)
        
        if not cached_code or cached_email != email:
            flash("请先获取并输入正确的验证码！")
            return redirect(url_for("auth.register"))
            
        if time.time() - cached_time > 300:
            flash("验证码已过期，请重新获取！")
            return redirect(url_for("auth.register"))
            
        if cached_code != code:
            flash("验证码错误，请重新输入！")
            return redirect(url_for("auth.register"))
            
        if User.query.filter_by(email=email).first():
            flash("该邮箱已注册，请直接登录！")
            return redirect(url_for("auth.register"))
            
        if User.query.filter_by(student_id=form.student_id.data).first():
            flash("该学号已被注册")
            return redirect(url_for("auth.register"))
            
        # Clean session
        session.pop("verify_code", None)
        session.pop("verify_email", None)
        session.pop("code_time", None)
        
        user = User(
            student_id=form.student_id.data,
            nickname=form.nickname.data,
            contact_info=form.contact_info.data,
            email=email,
            password_hash=generate_password_hash("passwordless_default_hash")
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功，请登录！")
        return redirect(url_for("auth.login"))
        
    return render_template("register.html", form=form)

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        code = form.code.data
        
        # Verify code in session
        cached_code = session.get("verify_code")
        cached_email = session.get("verify_email")
        cached_time = session.get("code_time", 0)
        
        if not cached_code or cached_email != email:
            flash("请先获取并输入正确的验证码！")
            return redirect(url_for("auth.login"))
            
        if time.time() - cached_time > 300:
            flash("验证码已过期，请重新获取！")
            return redirect(url_for("auth.login"))
            
        if cached_code != code:
            flash("验证码错误，请重新输入！")
            return redirect(url_for("auth.login"))
            
        user = User.query.filter_by(email=email).first()
        if user:
            # Clean session
            session.pop("verify_code", None)
            session.pop("verify_email", None)
            session.pop("code_time", None)
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("用户不存在，请先注册！")
            return redirect(url_for("auth.register"))
            
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))