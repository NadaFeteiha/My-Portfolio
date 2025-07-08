# from peewee import *
# from datetime import datetime
# from flask import Flask, request
# from playhouse.shortcuts import model_to_dict
# import app

# class TimelinePost(Model):
#     name = CharField()
#     email = CharField()
#     content = TextField()
#     created_at = DateTimeField(default=datetime.now)

#     class Meta:
#         database = mydb

# mydb.connect()
# mydb.create_tables([TimelinePost])


# @app.route('/api/timeline_post', methods=['POST'])
# def post_time_line_post():
#     name = request.form['name']
#     email = request.form['email']
#     content = request.form['content']
    
#     timeline_post = TimelinePost.create(name=name, email=email, content=content)
#     return model_to_dict(timeline_post)


# @app.route('/api/timeline_post', methods=['GET'])
# def get_time_line_post():
#     return {
#         'timeline_posts': [
#             model_to_dict(p)
#             for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
#         ]
#     }
