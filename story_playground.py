import sys
import os
import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# lemmatizer = WordNetLemmatizer()

# print(lemmatizer.lemmatize("cats"))
# print(lemmatizer.lemmatize("cacti"))
# print(lemmatizer.lemmatize("geese"))
# print(lemmatizer.lemmatize("rocks"))
# print(lemmatizer.lemmatize("python"))
# print(lemmatizer.lemmatize("better", pos="a"))
# print(lemmatizer.lemmatize("best", pos="a"))
# print(lemmatizer.lemmatize("run"))
# print(lemmatizer.lemmatize("run",'v'))

cwd = os.getcwd()
story = open(cwd + '/developset/1999-W02-5.story', encoding='UTF-8')
story = story.read()
story = story.replace('\n',' ')
sep = 'TEXT: '
rest = story.split(sep, 1)[1]
storylines = sent_tokenize(story)
print(storylines)
dictlines = [[] for i in range(storylines.__len__())]
for i,sent in enumerate(storylines):
    dictlines[i]=word_tokenize(sent)
# print(dictlines)

# STEMMING
# print("after stemming")
# ps = PorterStemmer()
# for line in dictlines:
#     for sent in line:
#         print(ps.stem(sent))

# # Remove stop words
# print("Filtering stop words")
# stopsWords = set(stopwords.words('english'))
# print(stopsWords)
# wordsFiltered = []
# for line in dictlines:
#     for w in line:
#         if w not in stopsWords:
#             # This "w" here needs to be case insenstive
#             wordsFiltered.append(w)

# print(wordsFiltered)

for line in dictlines:
    for sent in line:
        print(nltk.pos_tag(nltk.word_tokenize(sent)))