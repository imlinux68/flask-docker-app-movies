from flask import Flask, render_template, request
import requests
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB container
DOMAIN = 'mongodb'
PORT = 27017
client = MongoClient(
        host = [ str(DOMAIN) + ":" + str(PORT) ],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
        username = "admin",
        password = "root",
    )

db = client["movies"]
collection = db["movies"]

# TMDB API key
TMDB_API_KEY = "a547e37479ae9d062d16fdcebbaad18f"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_movie():
    # Get movie name from search bar
    movie_name = request.form['movie_name']

    # Search for movie in MongoDB
    movie = collection.find_one({"name": movie_name})
    if movie:
        # If movie exists in MongoDB, return movie name and poster
        movie_name = movie['name']
        movie_poster = movie['poster']
        return render_template('result.html', movie_name=movie_name, movie_poster=movie_poster)
    else:
        # If movie doesn't exists in MongoDB, retrieve movie from TMDB API
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
        response = requests.get(url)
        data = response.json()
        if data['results']:
            # If movie exists in TMDB, insert movie poster and name to MongoDB
            movie_name = data['results'][0]['title']
            movie_poster = f"https://image.tmdb.org/t/p/w500/{data['results'][0]['poster_path']}"
            collection.insert_one({"name": movie_name, "poster": movie_poster})
            return render_template('result.html', movie_name=movie_name, movie_poster=movie_poster)
        else:
            # If movie doesn't exists in TMDB, return error message
            return render_template('result.html', error_message="Movie not found")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
