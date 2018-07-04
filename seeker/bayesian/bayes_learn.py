from seeker.logger import logger
from seeker.bayesian.bayes_db import bayes_db
from seeker.bayesian.bayes_words import list_to_dict
from seeker.bayesian.bayes_words import text_to_list


class bayes_learn():

    def __init__(self, category, sample):
        self.category = category
        self.sample = sample
        self.database = bayes_db()

    def learn(self):
        file_contents = None
        try:
            file_contents = open(self.sample, 'r').read()
        except Exception:
            logger.info("Failed to read sample file")
        word_list = text_to_list(file_contents)
        word_dict = list_to_dict(word_list)
        self.database.update_word(word_dict, self.category)
        logger.info("Finished learning \"%s\" from file: %s" % (self.category, self.sample))


if __name__ == '__main__':
    bayes_learn("virt-who", "./file_debug/f_pos").learn()
#     bayes_learn("others", "./file_debug/f_neg").learn()
