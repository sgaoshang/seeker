import time
import numpy as np
import naivebayes as nb

start = time.time()

# sample_file = './email/debug/sample.txt'
# sample_file = './email/training/sample.txt'
sample_file = './virtwho/virtwho_sample.txt'
text_words, text_label = nb.load_data(sample_file)
vocab_list = nb.set_vocabulary_list(text_words)
vectorized_word = nb.vectorize_words(text_words, vocab_list)
p_words_spamicity, p_words_hamicity, p_s = nb.train(vectorized_word, text_label)
nb.save_vocabulary_list(vocab_list)
# save p_words_spamicity, p_words_hamicity, p_s
np.savetxt('trained_model/p_words_spamicity.txt', p_words_spamicity, delimiter='\t')
np.savetxt('trained_model/p_words_hamicity.txt', p_words_hamicity, delimiter='\t')
with open('trained_model/p_s.txt', 'w') as f:
    f.write(p_s.__str__())

end = time.time()
print end - start
