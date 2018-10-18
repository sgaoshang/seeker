import os
import naivebayes as nb
from flask import current_app


def classify(component, text):
    model_path = current_app.config['NB_MODEL_PATH'] + component
    if os.path.exists(model_path):
        vocab_list, p_words_spamicity, p_words_hamicity, p_s = nb.get_trained_model(model_path)
        words = nb.pre_handle_text(text)
        return nb.single_classify(vocab_list, p_words_spamicity, p_words_hamicity, p_s, words)
    else:
        current_app.logger.info("No model exist for %s, just return 1..." % component)
        return 1
