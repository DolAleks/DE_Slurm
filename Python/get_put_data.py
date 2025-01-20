import requests
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import nltk
#nltk.download('punkt', force=True)
#nltk.download('stopwords', force=True)
#nltk.download('punkt', download_dir='~/nltk_data')
#nltk.download('stopwords', download_dir='~/nltk_data')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Подключение к PostgreSQL
def connect_to_db():
    return psycopg2.connect(
        host="localhost",
        port=5433,
        database="postgres",
        user="postgres",
        password="password"
    )

# Загрузка данных в PostgreSQL
def load_to_postgresql(table, data, conn):
    with conn.cursor() as cursor:
        execute_values(
            cursor,
            f"INSERT INTO {table} ({', '.join(data[0].keys())}) VALUES %s ON CONFLICT DO NOTHING",
            [tuple(d.values()) for d in data]
        )
    conn.commit()

# Функция для получения данных из YouTube API
def fetch_youtube_data(api_key, region="US", max_results=1000):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": region,
        "maxResults": max_results,
        "key": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        videos = response.json().get("items", [])
        return [
            {
                "video_id": video["id"],
                "title": video["snippet"]["title"],
                "category": video["snippet"]["categoryId"],
                "views": video["statistics"].get("viewCount", 0),
                "likes": video["statistics"].get("likeCount", 0),
                "comments": video["statistics"].get("commentCount", 0),
                "published_at": video["snippet"]["publishedAt"],
                "region": region,
                "trend_date": datetime.now().date()
            }
            for video in videos
        ]
    else:
        print(f"Error fetching YouTube data: {response.status_code}")
        return []

# Функция для получения данных из News API
def fetch_news(api_key, query="trending", max_results=100):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "pageSize": max_results,
        "sortBy": "publishedAt",
        "apiKey": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [
            {
                "title": article["title"],
                "source_name": article["source"]["name"],
                "published_at": article["publishedAt"],
                "url": article["url"],
                "content": article.get("content"),
                "youtube_video_id": None  # Обновим позже
            }
            for article in articles
        ]
    else:
        print(f"Error fetching News data: {response.status_code}")
        return []

# Функция извлечения ключевых слов
def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    keywords = [word for word in words if word.isalnum() and word not in stop_words]
    return set(keywords)

# Обогащение новостей ключевыми словами
def enrich_youtube_with_news(youtube_data, news_data):
    for news in news_data:
        news_keywords = extract_keywords(news["title"])
        for video in youtube_data:
            video_keywords = extract_keywords(video["title"])
            if news_keywords & video_keywords:
                news["youtube_video_id"] = video["video_id"]
                break
    return news_data

# Расчет метрик
def calculate_metrics(youtube_data, enriched_news_data):
    total_news = len(enriched_news_data)
    related_news = sum(1 for news in enriched_news_data if news["youtube_video_id"] is not None)
    videos_with_related_news = len(set(news["youtube_video_id"] for news in enriched_news_data if news["youtube_video_id"]))

    metrics = {
        "total_news": total_news,
        "related_news": related_news,
        "related_percentage": (related_news / total_news * 100) if total_news > 0 else 0,
        "videos_with_related_news": videos_with_related_news
    }
    return metrics

# Сохранение метрик в PostgreSQL
def save_metrics_to_db(metrics, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO project_metrics (metric_date, total_news, related_news, related_percentage, videos_with_related_news)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (metric_date) DO UPDATE
            SET total_news = EXCLUDED.total_news,
                related_news = EXCLUDED.related_news,
                related_percentage = EXCLUDED.related_percentage,
                videos_with_related_news = EXCLUDED.videos_with_related_news;
            """,
            (
                datetime.now().date(),
                metrics["total_news"],
                metrics["related_news"],
                metrics["related_percentage"],
                metrics["videos_with_related_news"]
            )
        )
    conn.commit()

# Основной скрипт
def main():
    youtube_api_key = "<youtube_api_key>"
    news_api_key = "<news_api_key>"

#    print(nltk.data.path)
    
    query = "trending on YouTube"

    # Подключение к базе данных
    conn = connect_to_db()

    try:
        # Получение данных
        youtube_data = fetch_youtube_data(youtube_api_key)
        news_data = fetch_news(news_api_key, query=query)

        # Обогащение новостей
        enriched_news_data = enrich_youtube_with_news(youtube_data, news_data)

        # Расчет метрик
        metrics = calculate_metrics(youtube_data, enriched_news_data)
        print(f"Metrics: {metrics}")

        # Сохранение метрик
        save_metrics_to_db(metrics, conn)

        # Загрузка данных в PostgreSQL
        if youtube_data:
            load_to_postgresql("youtube_trends", youtube_data, conn)
        if enriched_news_data:
            load_to_postgresql("news_articles", enriched_news_data, conn)

        print("Данные успешно загружены и метрики сохранены!")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        conn.close()

#if __name__ == "__main__":
main()
