from re import sub
from random import choice

garbage_words = ['verse', 'chorus', 'intro', 'hook', 'bridge', 'outro', 'proof']


def create_garbage_words_regex(excluded_words):
    return f"(.*(({')|('.join(excluded_words)})).*)"


def parse_text(text):
    garbage_words_regex = create_garbage_words_regex(garbage_words)
    text_without_punctuation = sub(r"(?![\w'’,]+).", ' ', text.lower())
    text_without_garbage = sub(garbage_words_regex, '', text_without_punctuation)
    words_list = sub(r'\s+', ' ', text_without_garbage).split(' ')
    return list(filter(lambda w: len(w) > 1, words_list))


def create_bigrams_dictionary(words):
    bigrams = {}
    for word_id in range(0, len(words) - 1):
        word = words[word_id]
        if word not in bigrams.keys():
            bigrams[word] = []
        bigrams[word].append(words[word_id + 1])
    return bigrams


def generate_text_from_bigrams(bigrams, line_length, lines_count):
    lines = []
    for line in range(0, lines_count):
        line = [choice(list(bigrams.keys()))]
        for word_index in range(1, line_length):
            line.append(choice(bigrams[line[word_index - 1]]))
        lines.append(line)
    return lines


def apply_capitalize(lines):
    words_to_capitalize = ["i'm", "i've", "i'd", "i'll", "i`m", "i`ve", "i`d", "i`ll"]
    result = []
    for line in lines:
        line[0] = line[0].capitalize()
        for index, word in enumerate(line):
            if word in words_to_capitalize:
                line[index] = word.capitalize()
        result.append(' '.join(line))
    return result


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
    return '\n'.join(set_punctuation(apply_capitalize(rap_lines)))


eminem_lyrics = open('lyrics.txt', 'r', encoding='utf-8')
rap = generate_rap(eminem_lyrics.read())
print(rap)
eminem_lyrics.close()
