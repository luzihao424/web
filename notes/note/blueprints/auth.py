from flask import render_template, redirect, url_for, flash, request, session, current_app, jsonify
from flask_login import login_user, logout_user
from core.extensions import db, supabase
from note.models import User
from note.forms import RegisterForm, LoginForm
from . import auth_bp

@auth_bp.route("/send-code", methods=["POST"])
def send_code():
    import random
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    if not email:
        return jsonify({"success": False, "message": "邮箱地址不能为空！"})
    
    # 验证邮箱是否已被注册
    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "message": "该邮箱已被注册，请直接登录或更换邮箱！"})
        
    code = random.randint(100000, 999999)
    session["register_email"] = email
    session["register_code"] = str(code)
    
    # 模拟发送验证码，将验证码打印到控制台，以便开发调试
    print("\n" + "=" * 50)
    print(f"【校园闲置时光胶囊】注册验证码")
    print(f"发送目标：{email}")
    print(f"您的6位验证码为：{code} (有效期至会话结束)")
    print("=" * 50 + "\n")
    
    return jsonify({"success": True, "message": "验证码已成功发送！"})

@auth_bp.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        password = form.password.data
        nickname = form.nickname.data
        email = form.email.data
        contact_info = form.contact_info.data
        input_code = form.verification_code.data
        
        # 0. 验证验证码是否正确
        session_email = session.get("register_email")
        session_code = session.get("register_code")
        
        if not session_email or session_email != email:
            flash("邮箱与发送验证码的邮箱不一致！")
            return render_template("register.html", form=form)
            
        if not session_code or session_code != input_code:
            flash("验证码不正确，请重新输入！")
            return render_template("register.html", form=form)
        
        # 1. 验证学号是否已存在
        if User.query.filter_by(student_id=student_id).first():
            flash("该学号已被注册，请直接登录！")
            return render_template("register.html", form=form)
            
        # 2. 验证昵称是否已存在
        if User.query.filter_by(nickname=nickname).first():
            flash("该昵称已被使用，请换一个昵称！")
            return render_template("register.html", form=form)
            
        # 3. 验证邮箱是否已存在
        if User.query.filter_by(email=email).first():
            flash("该邮箱已被注册，请直接登录或更换邮箱！")
            return render_template("register.html", form=form)

        try:
            # 尝试通过 Supabase 云端进行注册
            response = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "student_id": student_id,
                        "nickname": nickname,
                        "contact_info": contact_info
                    }
                }
            })

            # 创建新用户（在线模式，密码委托给 Supabase，本地 password_hash 留空）
            user = User(
                student_id=student_id,
                nickname=nickname,
                contact_info=contact_info,
                email=email,
                password_hash=""
            )
            db.session.add(user)
            db.session.commit()
            
            # 清理会话缓存
            session.pop("register_email", None)
            session.pop("register_code", None)
            
            flash("注册成功，请前往邮箱查收激活确认邮件！")
            return redirect(url_for("auth.login"))

        except Exception as e:
            db.session.rollback()
            err_msg = str(e).lower()
            # 在开发环境下，若遇到网络连接超时或网络受限导致握手失败，则自动降级为本地离线数据库注册
            if current_app.config.get("DEBUG") and ("timeout" in err_msg or "connection" in err_msg or "handshake" in err_msg or "ssl" in err_msg):
                try:
                    from werkzeug.security import generate_password_hash
                    # 本地离线注册：将密码在本地直接加密保存
                    user = User(
                        student_id=student_id,
                        nickname=nickname,
                        contact_info=contact_info,
                        email=email,
                        password_hash=generate_password_hash(password)
                    )
                    db.session.add(user)
                    db.session.commit()
                    
                    # 清理会话缓存
                    session.pop("register_email", None)
                    session.pop("register_code", None)
                    
                    flash("⚠️ 提示：云端网络连接超时，已自动降级为本地离线模式，免激活注册成功！请直接登录。")
                    return redirect(url_for("auth.login"))
                except Exception as local_err:
                    db.session.rollback()
                    flash(f"本地降级注册失败：{str(local_err)}")
                    return render_template("register.html", form=form)
            else:
                flash(f"注册失败：{str(e)}")
                return render_template("register.html", form=form)
            
    return render_template("register.html", form=form)

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        password = form.password.data
        
        user = User.query.filter_by(student_id=student_id).first()
        if not user:
            flash("该学号未注册，请先注册！")
            return redirect(url_for("auth.login"))

        try:
            # 尝试通过 Supabase 进行在线密码校验
            session_data = supabase.auth.sign_in_with_password({
                "email": user.email,
                "password": password
            })

            login_user(user)
            flash("登录成功！")
            return redirect(url_for("index"))
        
        except Exception as e:
            err_msg = str(e).lower()
            # 在开发环境下，如果云端连接超时，或者是之前已通过本地离线模式注册的用户（password_hash 不为空）
            if current_app.config.get("DEBUG"):
                from werkzeug.security import check_password_hash
                # 情况 A：如果该账号在本地存有加密密码，直接使用本地密码进行比对登录
                if user.password_hash and check_password_hash(user.password_hash, password):
                    login_user(user)
                    flash("⚠️ 提示：云端连接超时/账户未激活，已自动降级为本地密码比对，登录成功！")
                    return redirect(url_for("index"))
                
                # 情况 B：网络超时，但此前是用本地密码存储的普通账户
                if "timeout" in err_msg or "connection" in err_msg or "handshake" in err_msg or "ssl" in err_msg:
                    if user.password_hash and check_password_hash(user.password_hash, password):
                        login_user(user)
                        flash("⚠️ 提示：云端连接超时，已自动降级为本地密码比对，登录成功！")
                        return redirect(url_for("index"))
                        
            flash(f"登录失败,密码错误或账户未激活：{str(e)}")
            return redirect(url_for("auth.login"))
            
    return render_template("login.html", form=form)

@auth_bp.route("/logout")
def logout():
    try:
         supabase.auth.sign_out()
    except Exception as e:
        pass
    logout_user()
    flash("您已退出登录")
    return redirect(url_for("index"))