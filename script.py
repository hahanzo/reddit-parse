import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# enable the headless mode
options = Options()
options.add_argument('--headless')

# initialize a web driver to control Chrome
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)
# maxime the controlled browser window
driver.fullscreen_window()

# the URL of the target page to scrape
url = 'https://old.reddit.com/top/?sort=top&t=month'
# connect to the target URL in Selenium
driver.get(url)

# initialize the dictionary that will contain
# the subreddit scraped data
reddit = {}

# to store the post scraped data
posts = []

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
    
    author = post_html_element \
         .find_element(By.CLASS_NAME, "author") \
         .text
    
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
    post['comments'] = comments
    post['outbound_link'] = outbound_link

    # to avoid adding ad posts 
    # to the list of scraped posts
    # if title:
    posts.append(post)

reddit['posts'] = posts

# close the browser and free up the Selenium resources
driver.quit()

# export the scraped data to a JSON file
with open('subreddit.json', 'w', encoding='utf-8') as file:
    json.dump(reddit, file, indent=4, ensure_ascii=False)