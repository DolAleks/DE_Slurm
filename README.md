# DE_Slurm
## Финальное задание курса Data инженер - Поток 4

# Постановка задачи и ключевые моменты


## Цель проекта:

Создание системы анализа YouTube трендов и связанных новостей.

Построение пайплайна для извлечения, обработки и визуализации данных.


## Задачи:

- Автоматический сбор данных из двух источников: YouTube API и News API.
- Обогащение данных новостей информацией о видео (по ключевым словам).
- Расчет метрик для оценки качества обогащения.
- Визуализация данных и метрик в Superset.


## Использованные инструменты:

- PostgreSQL: хранение данных.
- Python: для API-запросов, обработки данных и расчета метрик.
- NLTK: для анализа текстов и выделения ключевых слов.
- Superset: для визуализации данных.
- Cron: для автоматизации запуска скриптов.
