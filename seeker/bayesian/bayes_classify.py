from __future__ import division
from seeker.logger import logger
from seeker.bayesian.bayes_db import bayes_db
from seeker.bayesian.bayes_words import text_to_list


class bayes_classify():

    MIN_WORD_COUNT = 5
    RARE_WORD_PROB = 0.5
    EXCLUSIVE_WORD_PROB = 0.99

    def __init__(self, sample, category1, category2):
        self.sample = sample
        self.category1 = category1
        self.category2 = category2
        self.database = bayes_db()

    def classify(self):
        word_list = self.__get_sample_word_list(self.sample)
        p_for_word_list = []
        self.category1_words_total = self.database.get_words_total(self.category1)
        self.category2_words_total = self.database.get_words_total(self.category2)
        for word in word_list:
            p_for_word_list.append(self.__get_p_for_word(word))
        result = self.__get_p_from_list(p_for_word_list)
        logger.info("Finished classifying, probability:%s, %s rather than %s" % (result, self.category1, self.category2))
        return result

    def __get_sample_word_list(self, sample):
        try:
            file_contents = open(sample, 'r').read()
            word_list = text_to_list(file_contents)
            if not len(word_list):
                logger.info('sample did not contain any valid words')
            return word_list
        except Exception:
            logger.info("Failed to read sample file")

    def __get_p_for_word(self, word):
        category1_word_count = self.database.get_word_count(self.category1, word)
        category2_word_count = self.database.get_word_count(self.category2, word)

        if category1_word_count + category2_word_count < self.MIN_WORD_COUNT:
            return self.RARE_WORD_PROB

        if category1_word_count == 0:
                return 1 - self.EXCLUSIVE_WORD_PROB
        elif category2_word_count == 0:
                return self.EXCLUSIVE_WORD_PROB
        # P(S|W) = P(W|S)P(S) / ( P(W|S)P(S) + P(W|H)P(H) )
        # P(S) = P(H) = 0.5
        # P(S|W) = P(W|S) / ( P(W|S) + P(W|H) )
        p_ws = category1_word_count / self.category1_words_total
        p_wh = category2_word_count / self.category2_words_total
        return p_ws / (p_ws + p_wh)

    def __get_p_from_list(self, l):
        # P = P1P2...P15 / ( P1P2...P15 + (1-P1)(1-P2)...(1-P15) )
        p_product = reduce(lambda x, y: x * y, l)
        p_inverse_product = reduce(lambda x, y: x * y, map(lambda x: 1 - x, l))
        return p_product / (p_product + p_inverse_product)


if __name__ == '__main__':
#     bayes_classify("./file_debug/f_pos", "virt-who", "others").classify()
    bayes_classify("./file_train/pos/01227475.txt", "virt-who-pos", "virt-who-neg").classify()
