import time
import requests
from django.core.management.base import BaseCommand
from home.models import Movie  # replace with your app name

OMDB_API_KEYS = [
    '5eeb4d2a',
    '57f88196',
    '31a51af6',
    '8e6ad8a0',
    'f34f41a',
    '9f9b4fd5',
    '1eddebb7',
    'cb14d3a4',
    'ea72618d'
]

OMDB_URL = 'http://www.omdbapi.com/'

class Command(BaseCommand):
    help = 'Fetch awards from OMDb and update movies'

    def handle(self, *args, **options):
        movies = Movie.objects.filter(awards__isnull=True).exclude(code__isnull=True)

        total = movies.count()
        print(f"Processing {total} movies without awards...")

        key_index = 0
        current_key = OMDB_API_KEYS[key_index]

        for i, movie in enumerate(movies, start=1):
            print(f"[{i}/{total}] Fetching awards for {movie.title} ({movie.code})")

            while True:
                try:
                    params = {
                        'apikey': current_key,
                        'i': movie.code,
                    }
                    response = requests.get(OMDB_URL, params=params, timeout=10)
                    data = response.json()

                    # Switch API key if limit reached
                    if data.get('Error') == 'Request limit reached!':
                        print(f"× API key {current_key} limit reached. Trying next key...")
                        key_index += 1
                        if key_index >= len(OMDB_API_KEYS):
                            print("× All API keys exhausted. Stopping.")
                            return
                        current_key = OMDB_API_KEYS[key_index]
                        continue  # Retry with new key

                    # No response or error
                    if data.get('Response') != 'True':
                        print(f"× OMDb Error: {data.get('Error', 'Unknown error')}")
                        break  # Don't retry, skip to next movie

                    # Save awards
                    awards = data.get('Awards', 'No awards info')
                    movie.awards = awards
                    movie.save()
                    print(f"→ Saved: {awards}")
                    break  # Move to next movie

                except Exception as e:
                    print(f"× Error for {movie.code}: {e}")
                    break  # Skip this movie

            time.sleep(1)  # Be polite to the server
