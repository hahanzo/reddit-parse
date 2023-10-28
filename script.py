import time
import json
import csv
import math
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# enable the headless mode
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-blink-features=AutomationControlled')

# initialize a web driver to control Chrome
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)
# maxime the controlled browser window
driver.fullscreen_window()

# to store the post scraped data
posts = []

def get_post_info(url):
    # connect to the target URL in Selenium
    driver.get(url)
    # retrieve the list of post HTML elements
    post_html_elements = driver \
        .find_elements(By.CSS_SELECTOR, '[class*="thing"]')

    for post_html_element in post_html_elements:
        # to store the data scraped from the
        # post HTML element
        post = {}

        # subreddit post scraping logic
        title = post_html_element \
            .find_element(By.CLASS_NAME, "title") \
            .text
        
        subreddit = post_html_element \
            .find_element(By.CLASS_NAME, "subreddit") \
            .text
        
        upvotes = post_html_element \
            .find_element(By.CLASS_NAME, "score.unvoted")  \
            .text
        
        try:
            author = post_html_element \
                .find_element(By.CLASS_NAME, "author") \
                .text
        except:
            author = '[Deleted]'
        
        datatime = post_html_element \
            .find_element(By.CLASS_NAME, "tagline") \
            .find_element(By.TAG_NAME, 'time') \
            .get_attribute('datetime')
        
        comments = post_html_element \
            .find_element(By.CLASS_NAME, "comments") \
            .text
        
        try:
            outbound_link = post_html_element \
                .find_element(By.CSS_SELECTOR, '[class*="outbound"]') \
                .get_attribute('href')
        except NoSuchElementException:
            outbound_link = None

        # populate the dictionary with the retrieved data
        post['title'] = title
        post['subreddit'] = subreddit
        post['upvotes'] = upvotes
        post['author'] = author
        post['datetime'] = datetime.fromisoformat(datatime).strftime('%Y-%m-%d %H:%M:%S')
        post['comments'] = comments
        post['outbound_link'] = outbound_link

        # to avoid adding ad posts 
        # to the list of scraped posts
        posts.append(post)

def scrape_subreddit(subreddit_url,page_amount,file_name):
    # initialize the page number
    page_number = 0
    # initialize the page URL
    page_url = subreddit_url

    driver.get(page_url)

    while page_number < page_amount:
        # get the post info for the current page
        get_post_info(page_url)
        
        page_number += 1
        
        time.sleep(2)
        # refresh page
        try:
            page_url = driver \
                .find_element(By.CSS_SELECTOR, 'span.next-button') \
                .find_element(By.TAG_NAME, 'a') \
                .get_attribute('href')
        except:
            print("no next page")
            break

        print("page",page_number)

    # export the scraped data to a JSON file
    with open(f'{file_name}.json', 'w', encoding='utf-8') as file:
        json.dump({'posts': posts}, file, indent=4, ensure_ascii=False)
    
    # Export the scraped data to a CSV file
    with open(f'{file_name}.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=posts[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(posts)
    # close the browser and free up the Selenium resources
    driver.quit()

# get 'top month' subreddit info
#scrape_subreddit('https://old.reddit.com/top/?sort=top&t=month',math.inf,'top_month_subreddit')
# get 'top year' subreddit info
#scrape_subreddit('https://old.reddit.com/top/?sort=top&t=year',math.inf,'top_year_subreddit')
# get 'top all' subreddit info
#scrape_subreddit('https://old.reddit.com/top/?sort=top&t=all',math.inf,'top_all_subreddit')

scrape_subreddit('https://old.reddit.com/r/popular/?geo_filter=GLOBAL',2,'popular_everywhera_subreddit')
scrape_subreddit('https://old.reddit.com/r/popular/?geo_filter=AR',2,'popular_ar_subreddit')