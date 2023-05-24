# Import libraries
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from collections import Counter
from selenium import webdriver



# Define the Page class
class Page:

    # Define the constructor
    def __init__(self, url):
        # Assign the url argument to an instance attribute
        self.url = url

    # Define the scrape method
    def scrape(self):
        # Get the page in selenium firefox webDriver
        driver.get(self.url)
        # Get the HTML page source
        page = driver.page_source
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(page, "html.parser")
        # Return the soup object
        return soup


# Define the JobPage class that inherits from Page
class JobPage(Page):

    # Define the constructor
    def __init__(self, url):
        # Call the parent constructor with the url argument
        super().__init__(url)
        # Create an empty Text object to store the text extracted from the web page
        self.text = Text()

    # Define the extract_text method
    def extract_text(self):
        # Call the parent scrape method and get the soup object
        soup = self.scrape()
        # Extract the text from the <div> element with class="jobDescription"
        text = soup.find("div", class_="o-box__text s-jobDesc c-pr40p").get_text()
        # Assign the text to the Text object's content attribute
        self.text.content = text


# Define the JobListPage class that inherits from Page
class JobListPage(Page):

    # Define the constructor
    def __init__(self, url):
        # Call the parent constructor with the url argument
        super().__init__(url)
        # Create an empty list to store the JobPage objects for each job link
        self.jobs = []

    # Define the extract_links method
    def extract_links(self):
        # Call the parent scrape method and get the soup object
        soup = self.scrape()
        # Find all the <a> elements with class="jobTitle"
        links = soup.find_all("a", {"class" : "c-jobListView__titleLink"})
        # Loop through each link element
        for link in links:
            # Get the href attribute of the <a> element
            href = link.get("href")
            # Create a JobPage object with the full URL as an argument
            job_page = JobPage(href)
            # Append the JobPage object to the jobs list
            self.jobs.append(job_page)


# Define the Text class that represents the text extracted from a web page
class Text:

    # Define the constructor
    def __init__(self):
        # Create an empty string to store the text content
        self.content = ""
        # Create an empty Counter object to store the word frequencies
        self.freq = Counter()

    # Define the process_text method
    def process_text(self):
        # Tokenize the content into words using NLTK
        words = word_tokenize(self.content)
        # Remove stopwords, punctuation, and numbers from the words
        stop_words = ['كسي', 'ريزي', 'رفت', 'گردد', 'مثل', 'آمد', 'ام', 'بهترين', 'دانست', 'كمتر', 'دادن', 'تمامي',
                      'جلوگيري', 'بيشتري', 'ايم', 'ناشي', 'چيزي', 'آنكه', 'بالا', 'بنابراين', 'ايشان', 'بعضي', 'دادند',
                      'داشتند', 'برخوردار', 'نخواهد', 'هنگام', 'نبايد', 'غير', 'نبود', 'ديده', 'وگو', 'داريم', 'چگونه',
                      'بندي', 'خواست', 'فوق', 'ده', 'نوعي', 'هستيم', 'ديگران', 'همچنان', 'سراسر', 'ندارند', 'گروهي',
                      'سعي', 'روزهاي', 'آنجا', 'يكديگر', 'كردم', 'بيست', 'بروز', 'سپس', 'رفته', 'آورده', 'نمايد',
                      'باشيم', 'گويند', 'زياد', 'خويش', 'همواره', 'گذاشته', 'شش  نداشته', 'شناسي', 'خواهيم', 'آباد',
                      'داشتن', 'نظير', 'همچون', 'باره', 'نكرده', 'شان', 'سابق', 'هفت', 'دانند', 'جايي', 'بی', 'جز',
                      'زیرِ', 'رویِ', 'سریِ', 'تویِ', 'جلویِ', 'پیشِ', 'عقبِ', 'بالایِ', 'خارجِ', 'وسطِ', 'بیرونِ', 'سویِ', 'کنارِ',
                      'پاعینِ', 'نزدِ', 'نزدیکِ', 'دنبالِ', 'حدودِ', 'برابرِ', 'طبقِ', 'مانندِ', 'ضدِّ', 'هنگامِ', 'برایِ', 'مثلِ',
                      'بارة', 'اثرِ', 'تولِ', 'علّتِ', 'سمتِ', 'عنوانِ', 'قصدِ', 'روب', 'جدا', 'کی', 'که', 'چیست', 'هست',
                      'کجا', 'کجاست', 'کَی', 'چطور', 'کدام', 'آیا', 'مگر', 'چندین', 'یک', 'چیزی', 'دیگر', 'کسی', 'بعری',
                      'جا', 'کس', 'هرگز', 'یا', 'تنها', 'بلکه', 'خیاه', 'بله', 'بلی', 'آره', 'آری', 'مرسی', 'البتّه',
                      'لطفاً', 'ّه', 'انکه', 'وقتیکه', 'همین', 'پیش', 'مدّتی', 'هنگامی', 'مان', '', 'نوع', 'همچنین',
                      'آنجا', 'قبل', 'جناح', 'اینها', 'طور', 'شاید', 'ایشان', 'جهت', 'طریق', 'مانند', 'پیدا', 'ممکن',
                      'کسانی', 'جای', 'کسی', 'غیر', 'بی', 'قابل', 'درباره', 'جدید', 'وقتی', 'اخیر', 'چرا', 'بیش',
                      'روی', 'طرف', 'جریان', 'زیر', 'آنچه', 'البته', 'فقط', 'چیزی', 'چون', 'برابر', 'هنوز', 'بخش',
                      'زمینه', 'بین', 'بدون', 'استفاد', 'همان', 'نشان', 'بسیاری', 'بعد', 'عمل', 'روز', 'اعلام', 'چند',
                      'آنان', 'بلکه', 'امروز', 'تمام', 'بیشتر', 'آیا', 'برخی', 'علیه', 'دیگری', 'ویژه', 'گذشته',
                      'انجام', 'حتی', 'داده', 'راه', 'سوی', 'ولی', 'زمان', 'حال', 'تنها', 'بسیار', 'یعنی', 'عنوان',
                      'پیش', 'وی', 'یکی', 'اینکه', 'وجود', 'شما', 'پس', 'چنین', 'میان', 'مورد', 'چه', 'اگر', 'همه',
                      'نه', 'دیگر', 'آنها', 'باید', 'هر', 'او', 'ما', 'من', 'تا', 'نیز', 'اما', 'یک', 'خود', 'بر', 'از',
                      'یا', 'هم', 'را', 'این', 'با', 'آن', 'برای', 'و', 'در', 'به', 'که', 'هیچ', 'همین', 'هبچ', 'چیز'] \
                        + stopwords.words("english") + \
                        list(string.punctuation) + ["’", "“", "”"]
        words = [word for word in words if word not in stop_words and word.isalpha()]
        # Calculate the frequency of each word using NLTK FreqDist and assign it to the freq attribute
        self.freq = nltk.FreqDist(words)
        global_freq.update(self.freq)

    # Define the get_keywords method that returns the top n most frequent words as keywords
    def get_keywords(self, n):
        return self.freq.most_common(n)


# ----------------------------------------------------------------

JobListPage_URL = 'https://jobinja.ir/jobs/category/it-software-web-development-jobs/' \
                  '%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85-%D9%88%D8%A8-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-' \
                  '%D9%86%D9%88%DB%8C%D8%B3-%D9%86%D8%B1%D9%85-%D8%A7%D9%81%D8%B2%D8%A7%D8%B1?&page='
global_freq = Counter()
driver = webdriver.Firefox(capabilities={"marionette": True})
try:
    for i in range(1, 3):
        try:
            URL = JobListPage_URL + str(i)
            job_list_page = JobListPage(URL)
            job_list_page.extract_links()
        except Exception as error:
            # handle the error
            print(error)
        for job_page in job_list_page.jobs:
            try:
                # job_page = JobPage(job_link)
                job_page.extract_text()
                job_page.text.process_text()
                print(job_page.text.get_keywords(6))

            except Exception as error:
                # handle the error
                print(error)

except Exception as error:
    # handle the error
    print(error)
print(global_freq.most_common(16))
