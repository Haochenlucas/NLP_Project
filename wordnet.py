from nltk.corpus import wordnet
import itertools
from nltk.corpus.reader import VERB
spring = wordnet.synsets("run")[0]
time = wordnet.synsets("operate")[0]
print(time.wup_similarity(spring))
#
# if not wordnet.synsets('Alice'):
#   print('Not an English Word')
# else:
#   print('English Word')
