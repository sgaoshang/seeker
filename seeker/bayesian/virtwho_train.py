import os
from bayes_learn import bayes_learn

pos_samples = os.listdir("file_train/pos")
for sample in pos_samples:
    bayes_learn("virt-who-pos", "./file_train/pos/%s" % sample).learn()
neg_samples = os.listdir("file_train/neg")
for sample in pos_samples:
    bayes_learn("virt-who-neg", "./file_train/neg/%s" % sample).learn()
