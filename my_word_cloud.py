# Import libraries
from persian_wordcloud.wordcloud import PersianWordCloud, add_stop_words
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def draw_only_en_word_cloud(dict):

    # Create a word cloud object
    wc = WordCloud(width=1280, height=720, max_words=200, background_color="white")
    # Generate the word cloud from the dictionary
    wc.generate_from_frequencies(dict)
    # Display the word cloud
    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(f'result2{next(iter(dict))}.png')


def draw_fa_en_word_cloud(dict):

    # Create a word cloud object
    wordcloud = PersianWordCloud(
        # only_persian=True,
        max_words=120,
        margin=0,
        width=1280,
        height=720,
        min_font_size=1,
        max_font_size=500,
        background_color="black")
    # Generate the word cloud from the dictionary
    wordcloud.generate_from_frequencies(dict)
    # Display the word cloud
    image = wordcloud.to_image()
    image.save(f'result{next(iter(dict))}.png')


def filter_eng_fa(freqs):
    # Convert the counter to a dictionary
    word_dict = dict(freqs)
    # Filter english words and persians
    eng_letters = set('abcdefghijklmnopqrstuvwxyz')
    eng_words_dict = {key: value for key, value in word_dict.items() if set(key.lower()).issubset(eng_letters)}
    persian_words_dict = {key: value for key, value in word_dict.items() if not set(key.lower()).issubset(eng_letters)}
    return eng_words_dict, persian_words_dict
