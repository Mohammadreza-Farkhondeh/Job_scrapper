from bs4 import BeautifulSoup
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import requests
from collections import Counter
import my_word_cloud
import pandas


class Page:
    def __init__(self, url):
        self.url = url

    def scrape(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0'}
        page = requests.get(self.url, headers=headers)
        html = page.text
        soup = BeautifulSoup(html, "html.parser")
        return soup

class JobPage(Page):

    def __init__(self, url):
        super().__init__(url)
        self.text = Text()

    def extract_text(self):
        soup = self.scrape()
        div = soup.find("div", class_="o-box__text s-jobDesc c-pr40p")
        if div:
            pass
        else:
            div = soup.find("div", class_="o-box__text s-jobDesc u-ltr c-pl40p")

        text = div.get_text()
        self.text.content = text

    def get_skill_tags(self):
        soup = self.scrape()
        lis = soup.find_all('li', {'class': "c-infoBox__item"})
        for li in lis:
            if li.find('h4').text == 'مهارت‌های مورد نیاز':  # If li was about skills, then find spans inside
                spans = li.find_all('span', {'class': 'black'})

        skills = []
        for span in spans:
            skills.append(span.text)

        return skills


class JobListPage(Page):

    def __init__(self, url):
        super().__init__(url)
        self.jobs = []

    def extract_links(self):
        soup = self.scrape()
        links = soup.find_all("a", {"class": "c-jobListView__titleLink"})
        for link in links:
            href = link.get("href")
            job_page = JobPage(href)
            self.jobs.append(job_page)


class Text:

    def __init__(self):
        self.content = ""
        self.freq = Counter()

    def process_text(self, method):
        words = word_tokenize(self.content)
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

        if method == 1:
            self.freq = FreqDist(words)

        elif method == 2:
            seen = set()
            self.freq = Counter()
            for word in words:
                if word not in seen:
                    seen.add(word)
                    self.freq[word] = 1

        global_freq.update(self.freq)

    def get_keywords(self, n):
        return self.freq.most_common(n)


def get_tags_to_DATA(skills):
    for skill in skills:
        if skill in DATA:
            DATA[skill] += 1
        else:
            DATA[skill] = 1


def export_tags():
    Sorted_DATA = {}
    sorted_list = sorted(DATA.items(), key=lambda item: int(item[1]), reverse=True)
    for i in sorted_list:
        Sorted_DATA.update({i[0]: i[1]})

    pandas.DataFrame(Sorted_DATA, index=[0]).T.to_csv('JOB_DATA_Jobinja.csv')


def get_most_common_freq(n):
    if n == '*':
        return global_freq
    elif isinstance(n, int):
        return global_freq.most_common(n)


def main():
    JobListPage_URL = 'https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B0%5D=data+engineering&filters%5Blocations%5D%5B0%5D=&filters%5Bjob_categories%5D%5B0%5D=&b=&page='
    global DATA
    DATA = {}
    page = 1
    global global_freq
    global_freq = Counter()

    try:
        for i in range(1, 16):
            try:
                URL = JobListPage_URL + str(i)
                job_list_page = JobListPage(URL)
                job_list_page.extract_links()
            except Exception as error:
                print(error)

            for job_page in job_list_page.jobs:
                try:
                    job_page.extract_text()
                    job_page.text.process_text(2)
                    skills = job_page.get_skill_tags()
                    get_tags_to_DATA(skills)
                    print(page)
                    page += 1
                except Exception as error:
                    print(error)

    except Exception as error:
        print(error)


def get_word_clouds():
    word_dict = dict(get_most_common_freq('*'))
    eng_words_dict, persian_words_dict = my_word_cloud.filter_eng_fa(word_dict)
    my_word_cloud.draw_fa_en_word_cloud(persian_words_dict)
    my_word_cloud.draw_fa_en_word_cloud(eng_words_dict)
    my_word_cloud.draw_only_en_word_cloud(eng_words_dict)


if __name__ == '__main__':
    print('Running...')
    main()
    get_word_clouds()
    export_tags()
