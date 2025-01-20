import requests
import psycopg2
from psycopg2.extras import execute_values

# Функция подключения к PostgreSQL
def connect_to_db():
    return psycopg2.connect(
        host="localhost",
        port=5433,
        database="postgres",
        user="postgres",
        password="password"
    )

# Функция для загрузки данных в PostgreSQL
def load_to_postgresql(table, data, conn):
    with conn.cursor() as cursor:
        execute_values(
            cursor,
            f"INSERT INTO {table} ({', '.join(data[0].keys())}) VALUES %s ON CONFLICT DO NOTHING",
            [tuple(d.values()) for d in data]
        )
    conn.commit()

def fetch_youtube_categories(api_key, region="US"):
    """Получение категорий видео из YouTube API"""
    url = "https://www.googleapis.com/youtube/v3/videoCategories"
    params = {
        "part": "snippet",
        "regionCode": region,
        "key": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        categories = response.json().get("items", [])
        return [
            {
                "category_id": category["id"],
                "category_name": category["snippet"]["title"]
            }
            for category in categories
        ]
    else:
        print(f"Error fetching categories: {response.status_code}")
        return []

def main():
    youtube_api_key = "<youtube_api_key>"

    # Подключение к базе данных
    conn = connect_to_db()

    try:
        # Получение категорий
        categories = fetch_youtube_categories(youtube_api_key)

        # Загрузка категорий в PostgreSQL
        if categories:
            load_to_postgresql("youtube_categories", categories, conn)
        print("Категории успешно загружены!")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()

#if __name__ == "__main__":
main()
