import time
import random
import numpy as np
import naivebayes as nb

start = time.time()

vocab_list, p_words_spamicity, p_words_hamicity, p_s = nb.get_trained_model()
test_file = './virtwho/virtwho_test.txt'
# test_file = './email/debug/test.txt'
text_words, text_label = nb.load_data(test_file)
nb.classify(vocab_list, p_words_spamicity, p_words_hamicity, p_s, text_words)

end = time.time()
print end - start
