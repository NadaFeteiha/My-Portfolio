from flask import Blueprint, render_template, redirect, url_for
from pathlib import Path
import os
import folium
from app.utils import load_json_data
import requests
from flask import request
from app.utils import format_date 
from app.TimelinePost import TimelinePost


main_pages = Blueprint('main_pages', __name__)

@main_pages.route('/')
def index():
    about_me = load_json_data(Path('app/static/json-data/aboutMe.json'), 'aboutMe')
    return render_template('index.html', name="Nada Feteiha", about_me=about_me, url=os.getenv("URL"))

@main_pages.route('/work')
def work():
    data = load_json_data(Path('app/static/json-data/experiences.json'), 'experiences')
    return render_template('work.html', title="Experience", experiences=data["work"], volunteers=data["volunteer"], url=os.getenv("URL"))

@main_pages.route('/projects')
def projects():
    data = load_json_data(Path('app/static/json-data/projects.json'), 'projects')
    print(f"Projects data loaded: {data}")
    return render_template('projects.html', title="Projects", projects=data, url=os.getenv("URL"))

@main_pages.route('/education')
def education():
    data = load_json_data(Path('app/static/json-data/education.json'), 'education')
    return render_template('education.html', title="Education", degrees=data["degrees"], certifications=data["certifications"], url=os.getenv("URL"))

@main_pages.route('/hobbies')
def hobbies():
    data = load_json_data(Path('app/static/json-data/hobbies.json'), 'hobbies')
    return render_template('hobbies.html', title="My Hobbies", hobbies=data, description="These are the activities that keep me inspired and energized.", url=os.getenv("URL"))

@main_pages.route('/map')
def map():
    places = load_json_data(Path('app/static/json-data/places.json'), 'places')

    folium_map = folium.Map(location=[40.7128, -74.0060], zoom_start=3)
    for place in places:
        folium.Marker(
            location=place["location"],
            tooltip=place["title"],
            popup=place["title"],
            icon=folium.Icon(icon="star", color="orange")
        ).add_to(folium_map)

    map_path = Path("app/static/maps/map.html")
    map_path.parent.mkdir(parents=True, exist_ok=True)
    folium_map.save(map_path)

    return render_template("map.html", places=places, title="Places I've Visited", description="The amazing places I've been to.", url=os.getenv("URL"))

#Updated Timeline code from Smriti to pass tests
@main_pages.route('/timeline')
def timeline():
    if os.getenv('TESTING') == 'true':
        # Use the local database in test mode
        posts_query = TimelinePost.select().order_by(TimelinePost.created_at.desc())
        posts = []
        for post in posts_query:
            posts.append({
                "name": post.name,
                "email": post.email,
                "content": post.content,
                "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "timeline_time": format_date(post.created_at.strftime('%a, %d %b %Y %H:%M:%S GMT'))

            })
    else:
        # Use the API in production
        url = os.getenv('URL')
        if not url:
            return "URL environment variable not set", 500

        response = requests.get(f"{url}/api/timeline_post")
        print(f"Response status code: {response}")
        posts = []
        try:
            response2 = response.json()
            posts = response2['timeline_posts']
            for post in posts:
                post['timeline_time'] = format_date(post['created_at'])
        except requests.exceptions.HTTPError as e:
            print("HTTP error:", e)
            print("Response text:", response.text)
        except requests.exceptions.JSONDecodeError:
            print("Invalid JSON response!")
            print("Raw response:", response.text)

    return render_template('timeline.html', title="Timeline", posts=posts, url=os.getenv("URL"))

# call the api to post a new timeline post
@main_pages.route('/timeline' , methods=['POST'])
def post_timeline():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    response = requests.post(
        f"{os.getenv('URL')}/api/timeline_post", 
        data={
            'name': name,
            'email': email,
            'content': content,
        }
    )

    if response.status_code == 200:
        post = response.json()
    else:
        print(f"Error posting to timeline: {response.status_code} - {response.text}")
    return redirect(url_for('main_pages.timeline'))
