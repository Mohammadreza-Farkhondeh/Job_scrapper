# Import libraries
import time
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver

# Define main url and driver
main_url = 'https://jobvision.ir/jobs/category/developer?page='
driver = webdriver.Chrome()

# Get jobs in pages first to 30th
for p in range(1, 30):
    # Get page url to driver and make soup
    page_url = main_url + str(p)
    driver.get(page_url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

