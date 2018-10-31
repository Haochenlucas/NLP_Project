import sys
import os
import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize, word_tokenize

cwd = os.getcwd()
story = open(cwd + '/project/NLP_project/developset/1999-W02-5.story', encoding='UTF-8')
story = story.read()
story = story.replace('\n',' ')
storylines = sent_tokenize(story)
print(storylines)
dictlines = [[] for i in range(storylines.__len__())]
for i,sent in enumerate(storylines):
    dictlines[i]=word_tokenize(sent)
print(dictlines)
for line in dictlines:
    for sent in line:
        print(nltk.pos_tag(nltk.word_tokenize(sent)))