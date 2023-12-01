import praw
import csv
import json

# Налаштування клієнта Reddit
reddit = praw.Reddit(client_id='your_client_id',
                     client_secret='your_client_secret',
                     user_agent='your_user_agent')

# Вибір популярного підreddit
subreddit = reddit.subreddit('popular')

# Створення порожніх списків для збереження метрик
post_metrics = []

# Ітерація через топ-пости популярного підreddit
for submission in subreddit.top(limit=10):  # Змініть limit на бажану кількість постів
    post_data = {
        'Title': submission.title,
        'Score': submission.score,
        'Number of comments': submission.num_comments
        # Додайте інші метрики, які вас цікавлять
    }
    post_metrics.append(post_data)

# Запис метрик у CSV файл
with open('post_metrics.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Score', 'Number of comments']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for post in post_metrics:
        writer.writerow(post)

# Запис метрик у JSON файл
with open('post_metrics.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(post_metrics, jsonfile, ensure_ascii=False, indent=4)