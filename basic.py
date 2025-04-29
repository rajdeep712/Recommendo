import requests
import time
from django.db.models import Q
from home.models import Movie  # Replace with your app name

TMDB_API_KEY = "fec0c8bd9ec35761aeef8b092da569df"

def get_tmdb_popularity(imdb_code, retries=3, base_delay=1):
    url = f"https://api.themoviedb.org/3/find/{imdb_code}"
    params = {
        "api_key": TMDB_API_KEY,
        "external_source": "imdb_id"
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("movie_results"):
                    return data["movie_results"][0].get("vote_count")
                else:
                    print(f"No movie_results for {imdb_code}")
            else:
                print(f"Non-200 response for {imdb_code}: {response.status_code}")
            break
        except requests.exceptions.ConnectionError as e:
            print(f"⚠️ Connection error on {imdb_code} (try {attempt+1}/{retries}): {e}")
            time.sleep(base_delay * (2 ** attempt))  # Exponential backoff

    print(f"❌ Failed after {retries} attempts: {imdb_code}")
    return None

def update_movies_popularity():
    movies = Movie.objects.filter(Q(vote_count__isnull=True) & ~Q(code=""))

    for movie in movies:
        print(f"\n🎬 Fetching: {movie.title} ({movie.code})")
        votecount = get_tmdb_popularity(movie.code)

        if votecount is not None:
            movie.vote_count = votecount
            movie.save()  # 🔥 Save right after fetching
            print(f"✅ Saved: {movie.title} -> {votecount}")
        else:
            print(f"⛔ Skipped: {movie.code}")

        time.sleep(0.3)  # Slow down to respect TMDB limits

    print("\n🎉 Done updating all movies!")
