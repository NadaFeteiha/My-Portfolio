from peewee import *
from datetime import datetime
from playhouse.shortcuts import model_to_dict 
from flask import request
from app.TimelinePost import TimelinePost
from flask import Blueprint, request
from app.utils import get_gravatar_profile

timeline_api = Blueprint('timeline_api', __name__)

@timeline_api.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    image = get_gravatar_profile(email)

    timeline_post = TimelinePost.create(name=name, email=email, content=content, image=image)
    return model_to_dict(timeline_post)


@timeline_api.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(post)
            for post in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


