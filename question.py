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
        questionFile = open(cwd + '/developset/' + questionFileName, encoding='UTF-8')
        questiontxt = questionFile.read().splitlines()
        questionFile.close()
        n = questiontxt.count('')
        while n > 0:
            questiontxt.remove('')
            n = n - 1
        self.questiontxt = questiontxt[1:len(questiontxt):3]
        self.questions = [[] for i in range(len(questiontxt))]
        self.questionsID = [None]*int(len(questiontxt)/3)
        for i,sent in enumerate(questiontxt):
            line = word_tokenize(sent)
            if(line[0] == "QuestionID"):
                self.questionsID[int(i/3)] = line[2]
            self.questions[i] = line[2:]
        self.questions = self.questions[1:len(self.questions):3]

    # categorize question type
    def categorize_question(self):
        return 

    # remove stop words
    def remove_stopwords(self, wordbags):
        stopsWords = set(stopwords.words('english'))
        bagsFiltered = []
        for bag in wordbags:
            wordsFiltered = []
            for w in bag:
                if w.lower() not in stopsWords:
                    # This "w" here needs to be case insenstive
                    wordsFiltered.append(w)
            bagsFiltered.append(wordsFiltered)
        return bagsFiltered

    # steming words
    def stem_words(self, wordbags):
        ps = PorterStemmer()
        bagsStemmed = []
        for line in wordbags:
            wordsStemmed = []
            for w in line:
                wordsStemmed.append(ps.stem(w))
            bagsStemmed.append(wordsStemmed)
        return bagsStemmed

    # pos tagging
    def pos_tag(self, wordbags):
        for line in wordbags:
            for sent in line:
                print(nltk.pos_tag(nltk.word_tokenize(sent)))

    # # tag NP in the question
    # def ner_tagging(self):
    #     return

    def print_sents(self):
        print(self.questionsID)
        print(self.questions)

# Type of question
class QuestionType(Enum):
    who = 1
    what = 2
    when = 3
    where = 4
    why = 5
    how = 6
