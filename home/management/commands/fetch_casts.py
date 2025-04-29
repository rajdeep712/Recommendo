import requests
from django.core.management.base import BaseCommand
from home.models import Movie, Cast
from django.conf import settings

TMDB_API_KEY = '9f493533c923a05656cbb32d7f15683c'  # Replace with your actual TMDb API key

class Command(BaseCommand):
    help = 'Fetch casts for movies from TMDb and update the database'

    def handle(self, *args, **kwargs):
        for movie_id in range(9538, 9553):  # inclusive of 9632
            try:
                movie = Movie.objects.get(id=movie_id)

                if movie.code:
                    tmdb_id = self.get_tmdb_id_from_imdb(movie.code)
                else:
                    self.stdout.write(self.style.WARNING(f"Movie ID {movie_id} has no imdb_id. Skipping."))
                    continue

                if not tmdb_id:
                    self.stdout.write(self.style.WARNING(f"TMDb ID not found for IMDb ID {movie.code}"))
                    continue

                cast_data = self.get_cast_from_tmdb(tmdb_id)

                if cast_data:
                    for member in cast_data:
                        name = member.get('name')
                        image_url = f"https://image.tmdb.org/t/p/w500{member['profile_path']}" if member.get('profile_path') else None

                        cast_obj, created = Cast.objects.get_or_create(name=name, defaults={'image_url': image_url})

                        if not created and image_url and not cast_obj.image_url:
                            cast_obj.image_url = image_url
                            cast_obj.save()

                        movie.casts.add(cast_obj)

                    movie.save()
                    self.stdout.write(self.style.SUCCESS(f"Updated casts for movie ID {movie_id}: {movie.title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"No cast found for TMDb ID {tmdb_id}"))

            except Movie.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Movie ID {movie_id} does not exist"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing movie ID {movie_id}: {e}"))

    def get_tmdb_id_from_imdb(self, imdb_id):
        url = f"https://api.themoviedb.org/3/find/{imdb_id}"
        params = {
            "api_key": TMDB_API_KEY,
            "external_source": "imdb_id"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            movie_results = data.get("movie_results")
            if movie_results:
                return movie_results[0].get("id")
        return None

    def get_cast_from_tmdb(self, tmdb_id):
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits"
        params = {
            "api_key": TMDB_API_KEY
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('cast', [])
        return []
