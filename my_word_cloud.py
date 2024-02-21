from persian_wordcloud.wordcloud import PersianWordCloud, add_stop_words
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def draw_only_en_word_cloud(dict):

    wc = WordCloud(width=1280, height=720, max_words=200, background_color="white")
    wc.generate_from_frequencies(dict)
    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(f'result2_data_engineering{next(iter(dict))}.png')


def draw_fa_en_word_cloud(dict):

    wordcloud = PersianWordCloud(
        max_words=120,
        margin=0,
        width=1280,
        height=720,
        min_font_size=1,
        max_font_size=500,
        background_color="black")
    wordcloud.generate_from_frequencies(dict)
    image = wordcloud.to_image()
    image.save(f'result_data_engineering_{next(iter(dict))}.png')


def filter_eng_fa(freqs):
    word_dict = dict(freqs)
    eng_letters = set('abcdefghijklmnopqrstuvwxyz')
    eng_words_dict = {key: value for key, value in word_dict.items() if set(key.lower()).issubset(eng_letters)}
    persian_words_dict = {key: value for key, value in word_dict.items() if not set(key.lower()).issubset(eng_letters)}
    return eng_words_dict, persian_words_dict
