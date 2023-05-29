# Import libraries
from bs4 import BeautifulSoup
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import requests
from collections import Counter
import my_word_cloud
import pandas


# Define the Page class
class Page:

    # Define the constructor
    def __init__(self, url):
        # Assign the url argument to an instance attribute
        self.url = url

    # Define the scrape method
    def scrape(self):
        # Change user agent to firefox because python-requests is blocked by jobinja
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'}
        # Get the page by request
        page = requests.get(self.url, headers=headers)
        # Get the HTML page source
        html = page.text
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(html, "html.parser")
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
        # Extract the text from the <div> element with class="..." this class is for persian texts
        # Make sure to not fail in first try
        div = soup.find("div", class_="o-box__text s-jobDesc c-pr40p")
        # checking the div to not be None(if the content is english, class is differnt)
        if div:
            pass
        else:
            # finding new div
            div = soup.find("div", class_="o-box__text s-jobDesc u-ltr c-pl40p")

        text = div.get_text()
        # Assign the text to the Text object's content attribute
        self.text.content = text

    # Define the get skill method
    def get_skill_tags(self):
        # Call the parent scrape method and get the soup object
        soup = self.scrape()
        # Find all li item with specified class to find skill spans not gender and diploma
        lis = soup.find_all('li', {'class': "c-infoBox__item"})
        for li in lis:
            if li.find('h4').text == 'مهارت‌های مورد نیاز':  # If li was about skills, then find spans inside
                spans = li.find_all('span', {'class': 'black'})

        # Define skills list and append found spans to it
        skills = []
        for span in spans:
            skills.append(span.text)

        return skills


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
        links = soup.find_all("a", {"class": "c-jobListView__titleLink"})
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
    def process_text(self, method):
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
                      'یا', 'هم', 'را', 'این', 'با', 'آن', 'برای', 'و', 'در', 'به', 'که', 'هیچ', 'همین', 'هبچ', 'چیز',
                      'های','باشد', 'داشته', 'است', 'شده', 'ای', 'کردن', 'سال', 'می', 'میباشد', 'باشی', 'هاي', 'رو', 'مي'] \
                        + ['well', 'related', 'providing', 'like', 'skilled', 'a', 'technical', 'an', 'knowledge', 'you',
                           'take', 'product', 'team', 'teams', 'the', 'building', 'new', 'ideal', 'identify', 'strong'
                           'role', 'technology', 'provideing', 'join', 'best', 'tools', 'technical', 'emerging',
                           'existing', 'part', 'work', 'joining', 'looking', 'able', 'create', 'let','candidate',
                           'debugging', 'user', 'career', 'working', 'seeking', 'closely', 'standards','written',
                           'following','passion', 'creating', 'ability', 'project', 'skills', 'modern', 'way', 'us'] \
                        + list(stopwords.words("english")) + \
                        list(string.punctuation) + ["’", "“", "”"]
        words = [str(word.lower()) for word in words if word.lower() not in stop_words and word.isalpha()]

        # There is two method one get you number of repetitions, one get only existence of words
        if method == 1:
            # Calculate the frequency of each word using NLTK FreqDist and assign it to the freq attribute
            self.freq = FreqDist(words)

        elif method == 2:
            # Create an empty set and an empty dictionary
            seen = set()
            self.freq = Counter()
            # Loop through the words and assign a frequency of 1 to the new words
            for word in words:
                if word not in seen:
                    seen.add(word)
                    self.freq[word] = 1

        # Update the global_freq with the local freq
        global_freq.update(self.freq)

    # Define the get_keywords method that returns the top n most frequent words as keywords
    def get_keywords(self, n):
        return self.freq.most_common(n)


def get_tags_to_DATA(skills):
    # Append skills number to DATA
    for skill in skills:
        if skill in DATA:
            DATA[skill] += 1
        else:
            DATA[skill] = 1


def export_tags():
    # Sort Data
    Sorted_DATA = {}
    sorted_list = sorted(DATA.items(), key=lambda item: int(item[1]), reverse=True)
    for i in sorted_list:
        Sorted_DATA.update({i[0]: i[1]})

    # Export DATA to excel file
    pandas.DataFrame(Sorted_DATA, index=[0]).T.to_csv('JOB_DATA_Jobinja.csv')


def get_most_common_freq(n):
    if n == 'all':
        return global_freq
    elif type(n) is int:
        return global_freq.most_common(n)


def main():
    JobListPage_URL = 'https://jobinja.ir/jobs/category/it-software-web-development-jobs/' \
                      '%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85-%D9%88%D8%A8-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-' \
                      '%D9%86%D9%88%DB%8C%D8%B3-%D9%86%D8%B1%D9%85-%D8%A7%D9%81%D8%B2%D8%A7%D8%B1?&page='
    global DATA
    DATA = {}
    page = 1
    global global_freq
    global_freq = Counter()

    try:  # Get the  pages and frequencies
        for i in range(1, 199):
            try:
                URL = JobListPage_URL + str(i)  # Add page number to URL
                job_list_page = JobListPage(URL)
                job_list_page.extract_links()
            except Exception as error:
                # handle the error
                print(error)

            for job_page in job_list_page.jobs:  # Get the words and frequencies in job_page
                try:
                    job_page.extract_text()
                    job_page.text.process_text(2)
                    skills = job_page.get_skill_tags()
                    get_tags_to_DATA(skills)
                    print(page)
                    page += 1
                except Exception as error:
                    # handle the error
                    print(error)

    except Exception as error:
        # handle the error
        print(error)


def get_word_clouds():
    # Get the all words
    word_dict = dict(get_most_common_freq('all'))
    # Filter english words and persians
    eng_words_dict, persian_words_dict = my_word_cloud.filter_eng_fa(word_dict)
    my_word_cloud.draw_fa_en_word_cloud(persian_words_dict)
    my_word_cloud.draw_fa_en_word_cloud(eng_words_dict)
    my_word_cloud.draw_only_en_word_cloud(eng_words_dict)


if __name__ == '__main__':
    print('Running...')
    main()
    get_word_clouds()
    export_tags()
