from flask import Flask
from app.database import mydb
from app.TimelinePost import TimelinePost
from app.routes.timeline_api import timeline_api
from app.routes.main_routes import main_pages

def create_app():
    app = Flask(__name__)

    # connect and create DB
    try:
        mydb.connect()
        # mydb.drop_tables([TimelinePost])
        mydb.create_tables([TimelinePost])
    except Exception as e:
        print("Failed!!", e)

    app.register_blueprint(timeline_api)
    app.register_blueprint(main_pages)

    return app
