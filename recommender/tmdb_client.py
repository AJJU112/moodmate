import requests
import random

TMDB_API_KEY = "51506308c2d812b0cc119cb89f58f9ae"  # Replace with env var in production

def get_movies_by_mood(mood):
    mood_genres = {
        "happy": 35,     # Comedy
        "sad": 18,       # Drama
        "angry": 28,     # Action
        "chill": 10749   # Romance
    }

    genre_id = mood_genres.get(mood.lower())
    if not genre_id:
        return []

    # Random page from 1 to 5 (TMDB has many pages, but to avoid 404 keep it low)
    random_page = random.randint(1, 5)

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}&sort_by=popularity.desc&page={random_page}"

    try:
        response = requests.get(url)
        data = response.json()
        results = data.get("results", [])

        movie_data = [
            {
                "title": movie["title"],
                "url": f"https://www.themoviedb.org/movie/{movie['id']}",
                "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None,
                "rating": movie.get("vote_average", "N/A"),
                "release_year": movie.get("release_date", "N/A")[:4] if movie.get("release_date") else "N/A"
            }
            for movie in results[:6]
        ]
        return movie_data

    except Exception as e:
        print("API ERROR:", e)
        return []

