from peewee import *
from playhouse.shortcuts import model_to_dict 
from flask import request, Blueprint
from app.TimelinePost import TimelinePost
from app.utils import get_gravatar_profile

timeline_api = Blueprint('timeline_api', __name__)

@timeline_api.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')
    
    # Validate required fields and formats to match your tests
    #Smriti: Only had to make slight edits to ensure that the test would pass
    if not name or name.strip() == "":
        return "Invalid name", 400
    
    if not content or content.strip() == "":
        return "Invalid content", 400

    if not email or "@" not in email or "." not in email.split("@")[-1]:
        return "Invalid email", 400

    image = get_gravatar_profile(email)

    timeline_post = TimelinePost.create(
        name=name,
        email=email,
        content=content,
        image=image
    )

    return model_to_dict(timeline_post)

@timeline_api.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(post)
            for post in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }
