import click
from flask.cli import with_appcontext
from core.extensions import db

@click.command("init-db")
@with_appcontext
def init_db():
    db.drop_all()
    db.create_all()
    click.echo("数据库初始化完成！")