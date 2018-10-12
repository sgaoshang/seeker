import naivebayes as nb


def classify(text):
    vocab_list, p_words_spamicity, p_words_hamicity, p_s = nb.get_trained_model()
    words = nb.pre_handle_text(text)
    return nb.single_classify(vocab_list, p_words_spamicity, p_words_hamicity, p_s, words)
