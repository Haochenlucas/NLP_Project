import sys
import os
import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# This is the class to store story instance
class Story:
    # Maybe NER library as well
    def __init__(self, storyFileName):
        cwd = os.getcwd()
        storyFile = open(cwd + '/project/NLP_project/developset/' + storyFileName, encoding='UTF-8')
        story = storyFile.read()
        story = story.replace('\n',' ')
        cut = 'TEXT: '
        story = story.split(cut, 1)[1]
        self.sentences = sent_tokenize(story)
        storyFile.close()

        # score of each sentences for a single question
        # should be initialzed to 0 after answering a question
        self.score = []

    # word tokenize for sentences
    def word_tokenize(self):
        return

    # remove stop words
    def remove_stopwords(self):
        return

    # steming words
    def stem_words(self):
        return

    # pos tagging
    def pos_tag(self):
        return

    # # tage NP in the Story
    # def ner_tagging(sent):
    #     return

    # give score to all sentences based on the given question
    def update_score(self):
        return
    