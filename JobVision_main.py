# Import libraries
import time
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver

# Define main url and driver
main_url = 'https://jobvision.ir/jobs/category/developer?page='
driver = webdriver.Chrome()

# Define desired links list of links to jobs
desired_links = []

# Get jobs in pages first to 30th
for p in range(1, 30):
    # Get page url to driver and make soup
    page_url = main_url + str(p)
    driver.get(page_url)
    # time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # Get all links in the page and filter links to job pages,
    # append job links in the page to the full desired links
    all_links = list(soup.find_all('a'))
    for link_j in soup.select("a[id*='el-']"):
        desired_links.append(link_j['id'].split('-')[1])