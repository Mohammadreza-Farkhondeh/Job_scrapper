# Import libraries and Jobinja_main
from persian_wordcloud.wordcloud import PersianWordCloud, add_stop_words
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import Jobinja_main
import random


# Get freqs from Jobinja_main
freqs = Jobinja_main.get_most_common_freq(130)

# Convert the list to a dictionary
word_dict = dict(freqs)

# Filter english words and persians
eng_letters = set('abcdefghijklmnopqrstuvwxyz')
eng_words_dict = {key: value for key, value in word_dict.items() if set(key.lower()).issubset(eng_letters)}
persian_words_dict = {key: value for key, value in word_dict.items() if not set(key.lower()).issubset(eng_letters)}


# Define stopwords
stopwords = add_stop_words([])


def draw_only_en_word_cloud():

    # Create a word cloud object
    wc = WordCloud(width=800, height=400, max_words=200, background_color="white")
    # Generate the word cloud from the dictionary
    wc.generate_from_frequencies(eng_words_dict)
    # Display the word cloud
    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


def draw_fa_en_word_cloud(dict):

    # Create a word cloud object
    wordcloud = PersianWordCloud(
        # only_persian=True,
        max_words=100,
        stopwords=stopwords,
        margin=0,
        width=800,
        height=800,
        min_font_size=1,
        max_font_size=500,
        background_color="black")
    # Generate the word cloud from the dictionary
    wordcloud.generate_from_frequencies(dict)
    # Display the word cloud
    image = wordcloud.to_image()
    image.show()
    num = random.randint(1000, 9999)
    image.save(f'result{num}.png')


draw_fa_en_word_cloud(persian_words_dict)
draw_fa_en_word_cloud(eng_words_dict)
draw_only_en_word_cloud()