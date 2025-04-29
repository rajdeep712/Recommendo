import requests
import time
import psycopg2
from psycopg2.extras import execute_values

TMDB_API_KEY = 'fec0c8bd9ec35761aeef8b092da569df'

# PostgreSQL connection config
DB_CONFIG = {
    'dbname': 'django_college_kpiz',
    'user': 'django_college_kpiz_user',
    'password': 'H1wmTcVRxbhMq6zMEe7uIILcUxRIgKZs',
    'host': 'dpg-cvqpfovdiees739ncr00-a.oregon-postgres.render.com',
    'port': 5432
}

IMAGE_BASE = 'https://image.tmdb.org/t/p/original'

def fetch_and_insert_movies(year, max_count=500):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    added = 0
    print(f"🔍 Fetching for year: {year}")

    for page in range(1, 26):
        print(f"\n➡️ Page {page}")
        url = "https://api.themoviedb.org/3/discover/movie"
        params = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US',
            'region': 'IN',
            'sort_by': 'popularity.desc',
            'include_adult': 'false',
            'include_video': 'false',
            'page': page,
            'primary_release_year': year
        }

        try:
            r = requests.get(url, params=params)
            r.raise_for_status()
        except Exception as e:
            print(f"❌ Failed to fetch: {e}")
            continue

        for movie in r.json().get('results', []):
            if added >= max_count:
                break

            if movie.get('vote_average', 0.0) <= 6:
                continue

            tmdb_id = movie['id']
            try:
                ext = requests.get(
                    f"https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids",
                    params={'api_key': TMDB_API_KEY}
                ).json()
                imdb_id = ext.get('imdb_id')
                if not imdb_id:
                    continue

                details = requests.get(
                    f"https://api.themoviedb.org/3/movie/{tmdb_id}",
                    params={'api_key': TMDB_API_KEY}
                ).json()

                cur.execute("SELECT 1 FROM home_movie WHERE code = %s", (imdb_id,))
                if cur.fetchone():
                    continue  # Already exists

                poster_path = details.get('poster_path')
                poster_url = IMAGE_BASE + poster_path if poster_path else ''

                genres = ", ".join([g['name'] for g in details.get('genres', [])])
                overview = details.get('overview', '')

                insert_query = """
                    INSERT INTO home_movie
                    (code, title, year, rating, genres, poster, plot, popularity, vote_count)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(insert_query, (
                    imdb_id,
                    details.get('title'),
                    year,
                    details.get('vote_average'),
                    genres,
                    poster_url,
                    overview,
                    details.get('popularity'),
                    details.get('vote_count'),
                ))
                conn.commit()
                added += 1
                print(f"✅ Added: {details.get('title')}")

                time.sleep(0.3)

            except Exception as e:
                print(f"⚠️ Error saving: {e}")
                time.sleep(1)
                continue

        time.sleep(1)

    cur.close()
    conn.close()
    print(f"🎉 Done for {year}, Total added: {added}")

def run():
    for year in range(2023, 2026):
        fetch_and_insert_movies(year)

# Uncomment to run
run()
