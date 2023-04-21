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
for p in range(1, 2):
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


# Define skills list
skills = []

# Get job link by job id and reload driver
for job_id in desired_links:
    job_link = 'https://jobvision.ir/jobs/'+job_id
    driver.get(job_link)
    # Find skills in span in divs with requirement-value class
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    x = soup.find_all('div', {'class': "requirement-value bg-light py-2 px-3"})
    for div in x:
        spans = div.find_all('span', {'class': "tag-title font-weight-bold"})
        for span in spans:
            skills.append(span.text)

# Define most valuable variable DATA
DATA = {}

# Enrol skills to DATA dict
for skill in skills:
    if skill in DATA:
        DATA[skill] += 1
    else:
        DATA[skill] = 1
        