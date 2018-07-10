import time
import naivebayes as nb

start = time.time()

vocab_list, p_words_spamicity, p_words_hamicity, p_s = nb.get_trained_model()
test_file = './virtwho/debug/virtwho_test.txt'
# test_file = './email/debug/test.txt'
text_words, text_label = nb.load_data(test_file)
nb.classify(vocab_list, p_words_spamicity, p_words_hamicity, p_s, text_words)

end = time.time()
print end - start
# classify 10 case, training 600 case
# 2018-07-10 10:15:13,065 - seaker_logger - DEBUG - Succeeded to vectorize text words
# 2018-07-10 10:15:13,322 - seaker_logger - DEBUG - Classify result: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
# 200.32218504
# classify 10 case, training 100 case
# 2018-07-10 10:49:28,762 - seaker_logger - DEBUG - Succeeded to vectorize text words
# 2018-07-10 10:49:28,831 - seaker_logger - DEBUG - Classify result: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1]
# 89.3596060276
