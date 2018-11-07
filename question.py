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
        self.sent_POS = []
        self.answer_NP = []

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
            self.sent_POS.append(nltk.pos_tag(line))
        return self.sent_POS

    # # tage NP in the Story
    # def ner_tag(sent):
    #     return
    
    # Grouping NE
    def chuck_NE(self):
        grammar = r"""  
                NP: {<DT>?<JJ|JJR|VBN|VBG>*<CD><JJ|JJR|VBN|VBG>*<NNS|NN>+}
        {<DT>?<JJS><NNS|NN>?}
        {<DT>?<PRP|NN|NNS><POS><NN|NNP|NNS>*}
        {<DT>?<NNP>+<POS><NN|NNP|NNS>*}
        {<DT|PRP\$>?<RB>?<JJ|JJR|VBN|VBG>*<NN|NNP|NNS>+}
        {<WP|WDT|PRP|EX>}
        {<DT><JJ>*<CD>}
        {<\$>?<CD>+}
                """
        cp = nltk.RegexpParser(grammar)
        tree_ques = []
        np_tree = [[] for i in range(len(self.sent_POS))]
        np_chunk = [[] for i in range(len(self.sent_POS))]
        for i, ques in enumerate(self.sent_POS):
            tree_ques.append(cp.parse(ques))

        for i, line in enumerate(tree_ques):
            for NP in line:
                if (type(NP) is nltk.tree.Tree and NP._label == 'NP'):
                    np_tree[i].append(NP)

        for i, NP in enumerate(np_tree):
            for j, subNP in enumerate(NP):
                set = []
                for w in subNP:
                    set.append(w[0])
                s = ' '.join(set)
                np_chunk[i].append(s)
        # print(np_chunk)
        return np_chunk

    def print_sents(self):
        print(self.questionsID)
        print(self.questions)

    # Type of question

    # WHO
    # LOCATION (country is marked as location), PERSON, ORGANIZATION

    # WHAT
    # Everything is possible
    # Need to check the following NP and PP to narrow down
    # e.g. What is the time? -> TIME
    # e.g. What is the date today? -> DATE
    # e.g. What has A done with B? -> This will look for a sentence of explaination instead of just a simple NP.

    # WHEN
    # DATE, TIME

    # WHERE
    # LOCATION, ORGANIZATION (e.g. Where does he work?)

    # WHY
    # This will look for a sentence of explaination instead of just a simple NP.

    # HOW
    # This will look for a sentence of explaination instead of just a simple NP. or
    # How long -> TIME
    # How much -> MONEY
    # How many -> looking fo a number
    def answer_NP_type(self):
        for question in self.sent_POS:
            for word in question:
                tag = word[1]
                if (tag == "WDT" or tag == "WP" or tag == "WP$" or tag == "WRB"):
                    # This part can have a lot optimization
                    if(word[0].lower() == "who"):
                        self.answer_NP.append(["LOCATION", "PERSON", "ORGANIZATION"])
                    elif(word[0].lower() == "what"):
                        self.answer_NP.append(["EVERYTHING!!!"])
                    elif(word[0].lower() == "when"):
                        self.answer_NP.append(["DATA", "TIME"])
                    elif(word[0].lower() == "where"):
                        self.answer_NP.append(["LOCATION", "ORGANIZATION"])
                    elif(word[0].lower() == "why"):
                        self.answer_NP.append(["EVERYTHING"])
                    elif(word[0].lower() == "how"):
                        self.answer_NP.append(["MONEY", "TIME"])

    # NER Types:
    # LOCATION
    # ORGANIZATION
    # DATE
    # MONEY
    # PERSON
    # PERCENT
    # TIME