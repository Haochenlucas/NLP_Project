import sys
import os
import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from enum import Enum

class Question():
    def __init__(self, questionFileName):
        cwd = os.getcwd()
        questionFile = open(cwd + '/project/NLP_project/developset/' + questionFileName, encoding='UTF-8')
        question = questionFile.read().splitlines()
        n = question.count('')
        while n > 0:
            question.remove('')
            n = n - 1
        questionlines = [[] for i in range(len(question))]
        for i,sent in enumerate(question):
            questionlines[i] = word_tokenize(sent)
        self.questionlines = questionlines[1:len(questionlines):3]
        questionFile.close()

    # categorize question type
    def categorize_question(self):
        return 

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
    def pos_tagging(self):
        return

    # # tag NP in the question
    # def ner_tagging(self):
    #     return

# Type of question
class QuestionType(Enum):
    who = 1
    what = 2
    when = 3
    where = 4
    why = 5
    how = 6
