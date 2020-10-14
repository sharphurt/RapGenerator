import re
from random import choice, randint

garbage_words = ['verse', 'chorus', 'intro', 'hook', 'outro']


def create_garbage_words_regex(excluded_words):
    return f"(.*(({')|('.join(excluded_words)})).*)"


def parse_text(text):
    garbage_words_regex = create_garbage_words_regex(garbage_words)
    text_without_punctuation = re.sub(r"(?![\w'’]+).", ' ', text.lower())
    text_without_garbage = re.sub(garbage_words_regex, '', text_without_punctuation)
    words_list = re.sub(r'\s+', ' ', text_without_garbage).split(' ')
    return list(filter(lambda w: len(w) > 1, words_list))


def create_bigrams_dictionary(words):
    bigrams = {}
    for word_id in range(0, len(words) - 1):
        word = words[word_id]
        if word not in bigrams.keys():
            bigrams[word] = set()
        bigrams[word].add(words[word_id + 1])
    return bigrams


def generate_text_from_bigrams(bigrams, line_length=5, lines_count=10):
    lines = []
    for line in range(0, lines_count):
        line = [choice(list(bigrams.keys()))]
        for word in range(1, line_length):
            line.append(choice(list(bigrams[line[word - 1]])))
        lines.append(' '.join(line).capitalize())
    return lines


def set_commas(lines):
    result = []
    for line in lines:
        punct_symbols_count = randint(1, line.count(' ') // 2)
        for i in range(punct_symbols_count):
            whitespaces = list(filter(lambda p: p[1] == ' ', list(enumerate(line))))
            index = choice(whitespaces)[0]
            line = line[:index] + ',' + line[index:]
        result.append(re.sub(',+', ',', line))
    return result


def generate_rap(*base, line_length=10, lines_count=20):
    bigrams = {}
    for text in base:
        bigrams.update(create_bigrams_dictionary(parse_text(text.read())))
    return '\n'.join(set_commas(generate_text_from_bigrams(bigrams, line_length, lines_count)))


rap_god_text = open('rap_god.txt', 'r', encoding='utf-8')
lose_yourself_text = open('lose_yourself.txt', 'r', encoding='utf-8')
godzilla_text = open('godzilla.txt', 'r', encoding='utf-8')

rap = generate_rap(rap_god_text, lose_yourself_text, godzilla_text)
print(rap)

rap_god_text.close()
lose_yourself_text.close()
godzilla_text.close()
