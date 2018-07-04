import sqlite3
from seeker.logger import logger


class bayes_db():

    def __init__(self):
        self.conn = sqlite3.connect('../../instance/bayes.db')

    def update_word(self, word_dict, category):
        c = self.conn.cursor()
        try:
            for word, count in word_dict.items():
                c.execute('select count from word where category=? and word=?', (category, word))
                r = c.fetchone()
                if r:
                    c.execute('update word set count=? where category=? and word=?', (r[0] + count, category, word))
                else:
                    c.execute('insert into word (category, word, count) values (?,?,?)', (category, word, count))
        finally:
            c.close()
            self.conn.commit()

    def get_word_count(self, category, word):
        c = self.conn.cursor()
        try:
            c.execute('select count from word where category=? and word=?', (category, word))
            r = c.fetchone()
            if r:
                return r[0]
            else:
                return 0
        finally:
            c.close()
            self.conn.commit()

    def get_words_total(self, category):
        c = self.conn.cursor()
        try:
            c.execute('select sum(count) from word where category=?', (category,))
            r = c.fetchone()
            if r:
                return r[0]
            else:
                return 0
        finally:
            c.close()
            self.conn.commit()

    def reset(self):
        c = self.conn.cursor()
        try:
            c.execute('delete from word')
            c.execute('delete from category')
            logger.info("Succeed to reset bayes database")
        finally:
            c.close()
            self.conn.commit()


if __name__ == '__main__':
    bayes_db().reset()
