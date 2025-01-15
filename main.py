import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from importlib.metadata import version
print(version("flask"))
load_dotenv()

# Load API Key from .env file
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY must be set in the .env file")

app = Flask(__name__)

# Root route
@app.route("/")
def home():
    return "Welcome to the Flask App!"
# Test route to check if Flask is working
@app.route("/test")
def test():
    print("flask is working")
    return "Flask is working!"


@app.route("/movies", methods=["GET"])
def get_movies():
    year = request.args.get("year")
    page = request.args.get("page", 1, type=int)

    if not year or len(year) != 4 or not year.isdigit():
        return jsonify({"error": "Invalid year format. Use YYYY."}), 400

    try:
        # Discover Movie API Request
        discover_url = (
            f"https://api.themoviedb.org/3/discover/movie?language=en-US&primary_release_year={year}"
            f"&sort_by=popularity.desc&page={page}&api_key={TMDB_API_KEY}"
        )
        discover_response = requests.get(discover_url)
        discover_response.raise_for_status()
        movies = discover_response.json().get("results", [])

        result = []

        for movie in movies:
            movie_id = movie.get("id")
            movie_title = movie.get("title")
            release_date = movie.get("release_date")
            vote_average = movie.get("vote_average")

            # Movie Credit API Request
            editors = []
            try:
                credit_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}"
                credit_response = requests.get(credit_url)
                credit_response.raise_for_status()
                crew = credit_response.json().get("crew", [])
                editors = [person["name"] for person in crew if person.get("known_for_department") == "Editing"]
            except requests.RequestException:
                # Log or handle as needed, editors will remain empty if this fails
                pass

            result.append({
                "title": movie_title,
                "release_date": release_date,
                "vote_average": vote_average,
                "editors": editors
            })

        return jsonify(result)

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

# import flask
# print(flask.__version__)
import sys
print(sys.path)
