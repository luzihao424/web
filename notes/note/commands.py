import click
from flask.cli import with_appcontext
from core.extensions import db

@click.command("init-db")
@with_appcontext
def init_db():
    db.drop_all()
    db.create_all()
    click.echo("数据库初始化完成！")

@click.command("set-admin")
@click.argument("student_id")
@with_appcontext
def set_admin(student_id):
    from note.models import User
    user = User.query.filter_by(student_id=student_id).first()
    if not user:
        click.echo(f"错误：未找到学号为 '{student_id}' 的用户，请确认该用户已注册！")
        return
    user.is_admin = True
    db.session.commit()
    click.echo(f"成功：已将学号为 '{student_id}' 的用户（昵称：{user.nickname}）设为管理员！")