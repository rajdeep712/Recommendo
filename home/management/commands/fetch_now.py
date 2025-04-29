import time
import requests
from django.core.management.base import BaseCommand
from home.models import Movie
from django.db import transaction

TMDB_API_KEY = "9f493533c923a05656cbb32d7f15683c"

def get_tmdb_id(imdb_id):
    url = f"https://api.themoviedb.org/3/find/{imdb_id}"
    params = {"api_key": TMDB_API_KEY, "external_source": "imdb_id"}
    try:
        r = requests.get(url, params=params, timeout=10).json()
        movie_results = r.get("movie_results")
        if movie_results:
            return movie_results[0]["id"]
    except Exception as e:
        print(f"[Error] TMDB ID fetch failed for {imdb_id}: {e}")
    return None

def get_movie_details(tmdb_id):
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
    params = {"api_key": TMDB_API_KEY}
    try:
        r = requests.get(url, params=params, timeout=10).json()
        return {
            "budget": r.get("budget"),
            "revenue": r.get("revenue"),
            "runtime": r.get("runtime")
        }
    except Exception as e:
        print(f"[Error] Details fetch failed for TMDB ID {tmdb_id}: {e}")
        return None

class Command(BaseCommand):
    help = "Update budget, revenue, and runtime for movies using TMDb API"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.filter(budget__isnull=True, revenue__isnull=True, runtime__isnull=True)
        total = movies.count()
        self.stdout.write(f"Found {total} movies to update.")

        updated = 0
        for i, movie in enumerate(movies, 1):
            try:
                tmdb_id = get_tmdb_id(movie.code)
                if not tmdb_id:
                    continue

                details = get_movie_details(tmdb_id)
                if not details:
                    continue

                movie.budget = details["budget"]
                movie.revenue = details["revenue"]
                movie.runtime = details["runtime"]
                movie.save()

                updated += 1
                self.stdout.write(
                    f"[{i}/{total}] Updated: {movie.title} "
                    f"(Budget: {details['budget']}, Revenue: {details['revenue']}, Runtime: {details['runtime']} min)"
                )

                time.sleep(0.3)  # To respect rate limits

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error updating {movie.title}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Finished. {updated} movies updated."))