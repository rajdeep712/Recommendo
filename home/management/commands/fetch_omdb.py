import requests
import time
from django.core.management.base import BaseCommand
from home.models import Movie

# List of your OMDb API keys
OMDB_API_KEYS = [
    '5eeb4d2a',
    '57f88196',
    '31a51af6',
    '8e6ad8a0',
    'f34f41a',
    '9f9b4fd5',
    '1eddebb7',
    'cb14d3a4',
    'ea72618d',
    '16e3787'
]

current_key_index = 0

def get_next_key():
    global current_key_index
    current_key_index = (current_key_index + 1) % len(OMDB_API_KEYS)
    return OMDB_API_KEYS[current_key_index]

def fetch_ratings(imdb_id):
    global current_key_index
    retries = 0
    max_retries = len(OMDB_API_KEYS)

    while retries < max_retries:
        api_key = OMDB_API_KEYS[current_key_index]
        url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
        try:
            response = requests.get(url, timeout=10)
            data = response.json()

            # Check for API limit error
            if data.get("Error") == "Request limit reached!":
                print(f"[INFO] API key {api_key} limit reached. Switching key.")
                get_next_key()
                retries += 1
                continue

            imdb_rating = float(data.get("imdbRating", 0))
            imdb_votes = int(data.get("imdbVotes", "0").replace(",", ""))
            rt_rating = None

            for rating in data.get("Ratings", []):
                if rating["Source"] == "Rotten Tomatoes":
                    rt_rating = rating["Value"]
                    break

            return imdb_rating, imdb_votes, rt_rating

        except Exception as e:
            print(f"[ERROR] Failed to fetch ratings for {imdb_id} with key {api_key}: {e}")
            get_next_key()
            retries += 1

    return None, None, None

class Command(BaseCommand):
    help = "Fetch IMDb & Rotten Tomatoes ratings for all movies"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.filter(imdb_rating__isnull=True)
        total = movies.count()
        self.stdout.write(f"Updating ratings for {total} movies...")

        updated = 0
        for i, movie in enumerate(movies, 1):
            try:
                imdb_rating, imdb_votes, rt_rating = fetch_ratings(movie.code)
                if imdb_rating is not None:
                    movie.imdb_rating = imdb_rating
                    movie.imdb_votes = imdb_votes
                    movie.rotten_tomatoes = rt_rating
                    movie.save()
                    updated += 1
                    self.stdout.write(
                        f"[{i}/{total}] Updated {movie.title}: IMDb {imdb_rating}, Votes {imdb_votes}, RT {rt_rating}"
                    )
                time.sleep(0.2)  # Respect rate limits
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed: {movie.title} - {e}"))

        self.stdout.write(self.style.SUCCESS(f"Finished. {updated} movies updated."))
