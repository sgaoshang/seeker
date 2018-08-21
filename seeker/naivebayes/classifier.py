import naivebayes as nb
from seeker.logger import logger


def classify(text):
    vocab_list, p_words_spamicity, p_words_hamicity, p_s = nb.get_trained_model()
    words = nb.pre_handle_text(text)
    # logger.debug(words)
    return nb.single_classify(vocab_list, p_words_spamicity, p_words_hamicity, p_s, words)
