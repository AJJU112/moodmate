import requests # type: ignore

TMDB_API_KEY = "51506308c2d812b0cc119cb89f58f9ae"  # Your API Key

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

    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}&sort_by=popularity.desc"

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
        return [{"title": "API Error"}]

