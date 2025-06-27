import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
from pathlib import Path
import json
import folium

load_dotenv()
app = Flask(__name__)

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
    pathProjects = Path('app/static/json-data/projects.json')
    experiences = load_json_data(path, 'experiences')
    projects = load_json_data(pathProjects, 'projects')
    return render_template('work.html', title="Experience", experiences=experiences, projects=projects, url=os.getenv("URL"))

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