import re
from random import choice, randint

garbage_words = ['verse', 'chorus', 'intro', 'hook', 'bridge', 'outro', 'proof', '[', ']']


def create_garbage_words_regex(excluded_words):
    return f"(.*(({')|('.join(excluded_words)})).*)"


def parse_text(text):
    garbage_words_regex = create_garbage_words_regex(garbage_words)
    text_without_punctuation = re.sub(r"(?![\w'’,]+).", ' ', text.lower())
    text_without_garbage = re.sub(garbage_words_regex, '', text_without_punctuation)
    words_list = re.sub(r'\s+', ' ', text_without_garbage).split(' ')
    return list(filter(lambda w: len(w) > 1, words_list))


def create_bigrams_dictionary(words):
    bigrams = {}
    for word_id in range(0, len(words) - 1):
        word = words[word_id]
        if word not in bigrams.keys():
            bigrams[word] = []
        bigrams[word].append(words[word_id + 1])
    return bigrams


def generate_text_from_bigrams(bigrams, line_length=5, lines_count=10):
    lines = []
    words_to_capitalize = ["i'm", "i've", "i'd", "i'll", "i`m", "i`ve", "i`d", "i`ll"]
    for line in range(0, lines_count):
        line = [choice(list(bigrams.keys())).capitalize()]
        for word_index in range(1, line_length):
            next_word = choice(bigrams[line[word_index - 1].lower()])
            if next_word in words_to_capitalize:
                next_word = next_word.capitalize()
            line.append(next_word)
        lines.append(' '.join(line))
    return lines


def set_endline_marks(lines):
    result = lines.copy()
    marks = ['!', '?', ':', ';']
    passed_line_indexes = []
    for i in range(0, len(result)):
        index, line = choice(list(enumerate(result)))
        if index in passed_line_indexes:
            continue
        mark = choice(marks)
        result[index] = line + mark
        passed_line_indexes.append(index)
    return result


def set_punctuation(lines):
    return set_endline_marks(lines)


def generate_rap(*base, line_length=10, lines_count=20):
    bigrams = {}
    for text in base:
        bigrams.update(create_bigrams_dictionary(parse_text(text)))
    rap_lines = generate_text_from_bigrams(bigrams, line_length, lines_count)
    return '\n'.join(set_punctuation(rap_lines))


def insert_by_index(string, index, insert):
    str_list = list(string)
    str_list[index] = insert
    return ''.join(str_list)


eminem_lyrics = open('lyrics.txt', 'r', encoding='utf-8')

rap = generate_rap(eminem_lyrics.read())
print(rap)
eminem_lyrics.close()
