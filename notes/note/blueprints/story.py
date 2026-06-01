from flask import render_template
from note.models import TimeCapsuleStory
from . import story_bp

@story_bp.route("/wall")
def wall():
    stories = TimeCapsuleStory.query.order_by(TimeCapsuleStory.create_time.desc()).all()
    return render_template("story_wall.html", stories=stories)