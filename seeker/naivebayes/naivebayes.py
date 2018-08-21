import re
import numpy as np
from seeker.logger import logger


def pre_handle_text(text):
    # only words reserved
    regEx = re.compile(r'[^a-zA-Z]|\d')
    words = regEx.split(text)
    # lower words, strip blank
    words = [word.lower() for word in words if len(word) > 0]
    return words


def load_data(file_path):
    with open(file_path, 'r') as f:
        # text classification, eg. 1 as spam, 0 as ham
        text_label = []
        text_words = []
        for line in f.readlines():
            linedatas = line.strip().split('\t')
            if linedatas[0] == 'ham':
                text_label.append(0)
            elif linedatas[0] == 'spam':
                text_label.append(1)
            words = pre_handle_text(linedatas[1])
            text_words.append(words)
    return text_words, text_label


def set_vocabulary_list(text_words):
    vocabulary_set = set([])
    for words in text_words:
        vocabulary_set = vocabulary_set | set(words)
    vocab_list = list(vocabulary_set)
    logger.debug("Succeeded to generate vocabulary list")
    return vocab_list


def get_vocabulary_list(file_path):
    with open(file_path, 'r') as f:
        vocab_list = f.readline().strip().split('\t')
    return vocab_list


def save_vocabulary_list(vocab_list):
    with open('trained_model/vocab_list.txt', 'w') as f:
        for i in range(len(vocab_list)):
            f.write(vocab_list[i] + '\t')


def vectorize_words(text_words, vocab_list):
    vectorized_word_list = []
    for i in range(len(text_words)):
        vectorized_word = [0] * len(vocab_list)
        for word in text_words[i]:
            if word in vocab_list:
                vectorized_word[vocab_list.index(word)] += 1
        vectorized_word_list.append(vectorized_word)
    logger.debug("Succeeded to vectorize text words")
    return np.array(vectorized_word_list)


def train(train_words, train_label):
    num_samples = len(train_words)
    num_vocabulary = len(train_words[0])
    p_s = sum(train_label) / float(num_samples)  # P(S)

    spam_word_count = np.ones(num_vocabulary)
    ham_word_count = np.ones(num_vocabulary)
    spam_words_total = 2.0
    ham_words_total = 2.0
    for i in range(0, num_samples):
        if train_label[i] == 1:  # spam
            spam_word_count += train_words[i]
            spam_words_total += sum(train_words[i])
        else:
            ham_word_count += train_words[i]
            ham_words_total += sum(train_words[i])
    p_words_spamicity = np.log(spam_word_count / spam_words_total)
    p_words_hamicity = np.log(ham_word_count / ham_words_total)
    return p_words_spamicity, p_words_hamicity, p_s


def get_trained_model():
    vocab_list = get_vocabulary_list('seeker/naivebayes/trained_model/vocab_list.txt')
    p_words_spamicity = np.loadtxt('seeker/naivebayes/trained_model/p_words_spamicity.txt', delimiter='\t')
    p_words_hamicity = np.loadtxt('seeker/naivebayes/trained_model/p_words_hamicity.txt', delimiter='\t')
    with open('seeker/naivebayes/trained_model/p_s.txt', 'r') as f:
        p_s = float(f.readline().strip())
    return vocab_list, p_words_spamicity, p_words_hamicity, p_s


def classify(vocab_list, p_words_spamicity, p_words_hamicity, p_s, text_words):
    vectorized_word = vectorize_words(text_words, vocab_list)
    # logger.debug("Classify text: %s" % text_words)
    evaluated_label = []
    for item in vectorized_word[:]:
        # print item.shape
        # print p_words_spamicity.shape
        p1 = sum(item * p_words_spamicity) + np.log(p_s)
        p0 = sum(item * p_words_hamicity) + np.log(1 - p_s)
        if p1 > p0:
            evaluated_label.append(1)
        else:
            evaluated_label.append(0)
    logger.debug("Classify result: %s" % evaluated_label)
    return evaluated_label


def single_classify(vocab_list, p_words_spamicity, p_words_hamicity, p_s, text_word):
    vectorized_word = [0] * len(vocab_list)
    for word in text_word:
        if word in vocab_list:
            vectorized_word[vocab_list.index(word)] += 1
    np.array(vectorized_word)

    p1 = sum(vectorized_word * p_words_spamicity) + np.log(p_s)
    p0 = sum(vectorized_word * p_words_hamicity) + np.log(1 - p_s)
    if p1 > p0:
        evaluated_label = 1
    else:
        evaluated_label = 0
    logger.debug("Classify result: %s" % evaluated_label)
    return evaluated_label
