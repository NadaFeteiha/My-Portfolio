from peewee import *
from datetime import datetime
from playhouse.shortcuts import model_to_dict 
from flask import request
from app.TimelinePost import TimelinePost
from flask import Blueprint, request

timeline_api = Blueprint('timeline_api', __name__)

# route API
@timeline_api.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    
    if not name or not email or not content:
        return {"error": "Missing required fields"}, 400
    
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)


@timeline_api.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    print("Fetching timeline posts")
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }