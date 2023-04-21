# Import libraries
import time
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver

# Define main url and driver
main_url = 'https://jobvision.ir/jobs/category/developer?page='
driver = webdriver.Chrome()