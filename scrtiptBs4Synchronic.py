import json
import csv
import math
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    headers = {
        "User-Agent": "Your User Agent"
    }
    response = requests.get(url, headers=headers)
    return response.text

def get_post_info(html, posts):
    soup = BeautifulSoup(html, 'html.parser')

    post_elements = soup.select('[class*="thing"]')
    
    for post_element in post_elements:
        post = {}

        title = post_element.select_one('.title').get_text()
        subreddit = post_element.select_one('.subreddit').get_text()
        upvotes = post_element.select_one('.score.unvoted').get_text()
        
        try:
            author = post_element.select_one('.author').get_text()
        except AttributeError:
            author = '[Deleted]'

        datetime_element = post_element.select_one('.tagline time')
        datetime_attr = datetime_element['datetime']
        post_datetime = datetime.fromisoformat(datetime_attr).strftime('%Y-%m-%d %H:%M:%S')

        comments = post_element.select_one('.comments').get_text()
        
        outbound_link_element = post_element.select_one('[class*="outbound"]')
        outbound_link = outbound_link_element['href'] if outbound_link_element else None

        post['title'] = title
        post['subreddit'] = subreddit
        post['upvotes'] = upvotes
        post['author'] = author
        post['datetime'] = post_datetime
        post['comments'] = comments
        post['outbound_link'] = outbound_link

        posts.append(post)

def scrape_subreddit(subreddit_url, page_amount, file_name):
    posts = []
    page_number = 0
    page_url = subreddit_url

    start_time = time.time()  # Record the start time

    while page_number < page_amount:
        html = fetch_html(page_url)
        get_post_info(html, posts)

        page_number += 1
        next_button = BeautifulSoup(html, 'html.parser').select_one('span.next-button a')
        if next_button:
            page_url = next_button['href']
        else:
            break

        print("page", page_number)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time
    print(f"Scraping completed in {elapsed_time:.2f} seconds")

    with open(f'{file_name}.json', 'w', encoding='utf-8') as file:
        json.dump({'posts': posts}, file, indent=4, ensure_ascii=False)

    with open(f'{file_name}.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=posts[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(posts)

# Run the scraping tasks
if __name__ == '__main__':
    # scrape_subreddit('https://old.reddit.com/top/?sort=top&t=month', 100, 'month_subreddit')
    # scrape_subreddit('https://old.reddit.com/top/?sort=top&t=year', math.inf, 'top_year_subreddit')
    # scrape_subreddit('https://old.reddit.com/top/?sort=top&t=all', math.inf, 'top_all_subreddit')
    scrape_subreddit('https://old.reddit.com/',1500,'hot_everywhere_1500')
