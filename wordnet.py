from nltk.corpus import wordnet
spring = wordnet.synsets("a second")[0]
time = wordnet.synsets("period")[0]
print(time.wup_similarity(spring))
