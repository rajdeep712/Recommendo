import requests
import time
import psycopg2

TMDB_API_KEY = 'fec0c8bd9ec35761aeef8b092da569df'
IMAGE_BASE = 'https://image.tmdb.org/t/p/original'

# PostgreSQL connection info (edit this!)
DB_CONFIG = {
    'dbname': 'django_college_kpiz',
    'user': 'django_college_kpiz_user',
    'password': 'H1wmTcVRxbhMq6zMEe7uIILcUxRIgKZs',
    'host': 'dpg-cvqpfovdiees739ncr00-a.oregon-postgres.render.com',
    'port': 5432
}

def connect_db():
    return psycopg2.connect(**DB_CONFIG)

def movie_exists(cur, imdb_id):
    cur.execute("SELECT 1 FROM home_movie WHERE code = %s", (imdb_id,))
    return cur.fetchone() is not None

def insert_movie(cur, movie_data):
    query = """
        INSERT INTO home_movie
        (code, title, year, rating, genres, poster, plot, popularity, vote_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cur.execute(query, (
        movie_data['code'],
        movie_data['title'],
        movie_data['year'],
        movie_data['rating'],
        movie_data['genres'],
        movie_data['poster'],
        movie_data['plot'],
        movie_data['popularity'],
        movie_data['vote_count']
    ))

def fetch_and_insert_movies():
    conn = connect_db()
    cur = conn.cursor()

    added = 0
    year = 2025

    for page in range(1, 26):  # 25 pages x 20 movies/page = 500
        print(f"\n🔹 Page {page}")

        params = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US',
            'sort_by': 'popularity.desc',
            'include_adult': 'false',
            'include_video': 'false',
            'page': page,
            'primary_release_year': year,
            'region': 'IN'
        }

        try:
            res = requests.get("https://api.themoviedb.org/3/discover/movie", params=params)
            res.raise_for_status()
            movies = res.json().get('results', [])
        except Exception as e:
            print(f"❌ Failed to fetch page {page}: {e}")
            continue

        for movie in movies:
            try:
                tmdb_id = movie['id']
                ext_res = requests.get(f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids",
                                       params={'api_key': TMDB_API_KEY})
                imdb_id = ext_res.json().get('imdb_id')
                if not imdb_id:
                    continue

                if movie_exists(cur, imdb_id):
                    print(f"🔁 Already exists: {movie['title']}")
                    continue

                # Fetch full movie details
                details = requests.get(f"https://api.themoviedb.org/3/movie/{tmdb_id}",
                                       params={'api_key': TMDB_API_KEY}).json()

                poster_path = details.get('poster_path')
                poster_url = IMAGE_BASE + poster_path if poster_path else ''
                genres = ", ".join([g['name'] for g in details.get('genres', [])])

                movie_data = {
                    'code': imdb_id,
                    'title': details.get('title'),
                    'year': year,
                    'rating': details.get('vote_average', 0.0),
                    'genres': genres,
                    'poster': poster_url,
                    'plot': details.get('overview', ''),
                    'popularity': details.get('popularity'),
                    'vote_count': details.get('vote_count')
                }

                insert_movie(cur, movie_data)
                conn.commit()
                added += 1
                print(f"✅ Added: {movie_data['title']}")

            except Exception as e:
                print(f"⚠️ Error with movie: {movie.get('title')} - {e}")
                conn.rollback()
                continue

            time.sleep(0.25)  # Prevent hitting API rate limit

        time.sleep(1)

    print(f"\n🎉 Done. Total movies added: {added}")
    cur.close()
    conn.close()

# RUN
# Uncomment the line below to start
fetch_and_insert_movies()
