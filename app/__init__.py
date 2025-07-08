import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from pathlib import Path
import json
import folium
from peewee import *
from datetime import datetime
from playhouse.shortcuts import model_to_dict 

load_dotenv()

# Database configuration
# Step 1: Initialize MySQLDatabase with credentials
mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                    user=os.getenv("MYSQL_USER"),
                    password=os.getenv("MYSQL_PASSWORD"),
                    host=os.getenv("MYSQL_HOST"),
                    port=3306
                    )
print(mydb)


# # Step 2: Define the model
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb

# #  Step 3: Connect and create table
try:
    mydb.connect()
    mydb.create_tables([TimelinePost])
except Exception as e:
    print("⚠️ Failed to connect or create tables:", e)

# # Step 4: Initialize Flask app
app = Flask(__name__)

# # Step 5: Define routes for the API
@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    
    if not name or not email or not content:
        return {"error": "Missing required fields"}, 400
    
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)


@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    print("Fetching timeline posts")
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


def load_json_data(path: Path, category: str) -> list:
    try:
        with open(path, 'r', encoding = 'utf-8') as f:
            contents = json.load(f)
    except Exception as e:
        contents = []
        print(f'Error loading {category}: {e}')
    return contents

@app.route('/')
def index():
    path = Path('app/static/json-data/aboutMe.json')
    about_me = load_json_data(path, 'aboutMe')
    return render_template('index.html', name="Nada Feteiha", about_me=about_me, url=os.getenv("URL"))

@app.route('/work')
def work():
    path = Path('app/static/json-data/experiences.json')
    experiences = load_json_data(path, 'experiences')
    return render_template('work.html', title="Experience", experiences=experiences["work"],volunteers=experiences["volunteer"], url=os.getenv("URL"))

@app.route('/projects')
def projects():
    path = Path('app/static/json-data/projects.json')
    projects = load_json_data(path, 'projects')
    return render_template('projects.html', title="Projects", projects=projects, url=os.getenv("URL"))


@app.route('/education')
def education():
    path = Path('app/static/json-data/education.json')
    education = load_json_data(path, 'education')
    return render_template('education.html', title="Education", degrees=education["degrees"], certifications=education["certifications"], url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    path = Path('app/static/json-data/hobbies.json')
    hobbies = load_json_data(path, 'hobbies')
    return render_template('hobbies.html', title="My Hobbies", description="These are the activities that keep me inspired and energized outside of my professional work.", hobbies=hobbies, url=os.getenv("URL"))

@app.route('/map')
def map():
    path = Path('app/static/json-data/places.json')
    places = load_json_data(path, 'places')

    folium_map = folium.Map(location=[40.7128, -74.0060], zoom_start=3, min_zoom=3)
    add_markers(folium_map, places)

    # Save to static file
    map_path = Path("app/static/maps/map.html")
    Path.mkdir(map_path.parent, exist_ok=True)
    folium_map.save(map_path)

    return render_template("map.html", places=places, title="Places I've Visited", description="The amazing places I've been to.", url=os.getenv("URL"))

def add_markers(folium_map, places):
    for place in places:
        marker = folium.Marker(
            location=place["location"],
            tooltip=place["title"],
            popup=folium.Popup(place["title"], max_width=300),
            icon=folium.Icon(icon="star", color="orange", prefix='fa'),
            options={"autoPan": False}
        )
        marker.add_to(folium_map)