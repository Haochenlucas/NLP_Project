import sys
import os
import nltk
import re
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from enum import Enum
# os.environ['JAVAHOME'] = "D:/Java/jdk1.8.0_191/bin" #insert approriate version of jdk
os.environ['JAVAHOME'] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_102.jdk/Contents/Home" #insert approriate version of jdk
from nltk.tag import StanfordNERTagger

class Question():
    def __init__(self, questionFileName):
        # cwd = os.getcwd()
        # questionFile = open(cwd + '/developset/' + questionFileName, encoding='UTF-8')
        questionFile = open(questionFileName, encoding='UTF-8')
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

    def find_tag(self, NP):
        catg = list(list(zip(*NP))[1])
        word = list(list(zip(*NP))[0])
        if any(i == '$' for i in (catg)):
            word = [" ".join(word).lower()]
            word.append('MONEY')
        else:
            suspect = word[-1].lower()
            if not wordnet.synsets(suspect):
                # print('Not an English Word')
                word = [" ".join(word).lower()]
                word.append('none')
            else:
                suspect = wordnet.synsets(suspect)[0]
                typelist = ['period', 'organization', 'cost', 'person', 'place']
                max = [0.55, 'none']
                for ele in typelist:
                    type = wordnet.synsets(ele)[0]
                    value = 0
                    if type.wup_similarity(suspect) == None:
                        value = 0
                    else:
                        value = type.wup_similarity(suspect)
                    if max[0] < value:
                        max[0] = value
                        max[1] = ele
                word = [" ".join(word).lower()]
                word.append(max[1])
        return word

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
    def chuck_NP(self):
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
        return np_chunk


    def NER(self):
        # Find all NP that matches our grammar and put those in trees
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
        tree_S = []
        for i, ques in enumerate(self.sent_POS):
            tree_S.append(cp.parse(ques))

        # Use Stanfore NER to tag the all the words in the story
        ner_story =[[]for i in range(len(self.questions))]
        cwd = os.getcwd()
        eng_tagger = StanfordNERTagger(model_filename=cwd + '/stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
                path_to_jar=cwd + '/stanford-ner-2018-10-16/stanford-ner.jar')
        for i,sent in enumerate(self.questions):
            ner_story[i] = eng_tagger.tag(sent)
        # Put NE tag on the trees
        nerchunk_story = [[] for i in range(len(self.questions))]
        for i, line in enumerate(tree_S):
            start = 0
            for j, NP in enumerate(line):
                is_NER = 0
                if (type(NP) is nltk.tree.Tree and NP._label == 'NP'):
                    for l in range(start, start + len(NP)):
                        if ner_story[i][l][1] != 'O':
                            a = [" ".join(list(list(zip(*NP))[0]))]
                            a.append(ner_story[i][l][1])
                            nerchunk_story[i].append(a)
                            is_NER = 1
                            break
                    if is_NER == 0:
                        word = self.find_tag(NP)
                        nerchunk_story[i].append(word)
                    start += len(NP)
                else:
                    prop=[]
                    prop.append(NP[0])
                    prop.append(NP[1])
                    nerchunk_story[i].append(prop)
                    start += 1
        print(nerchunk_story)
        # nerchunk_story=[[]for i in range(len(self.questions))]
        # for i, line in enumerate(tree_S):
        #     start=0
        #     for j,NP in enumerate(line):
        #         if (type(NP) is nltk.tree.Tree and NP._label == 'NP'):
        #             for l in range(start,start+len(NP)):
        #                 if ner_story[i][l][1] != 'O':
        #                     nerchunk_story[i].append(NP)
        #                     nerchunk_story[i].append(ner_story[i][l][1])
        #                     break
        #
        #             start += len(NP)
        #         else:
        #             start += 1

        # Normalize out put of all marked NE
        # NPchunk_tagged = [[]for i in range(len(nerchunk_story))]
        # for k,sent in enumerate(nerchunk_story):
        #     for i,parse in  enumerate(sent):
        #         if (type(parse)==nltk.tree.Tree):
        #             leaf = parse.leaves()
        #             set = []
        #             for j,w in enumerate(leaf):
        #                 set.append(w[0])
        #             set.append(nerchunk_story[k][i + 1])
        #             NPchunk_tagged[k].append(set)
        return nerchunk_story

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
                        self.answer_NP.append(["LOCATION", "PERSON", "ORGANIZATION",'person'])
                    elif(word[0].lower() == "what"):
                        self.answer_NP.append(["EVERYTHING!!!"])
                    elif(word[0].lower() == "when"):
                        self.answer_NP.append(["DATA", "TIME",'period'])
                    elif(word[0].lower() == "where"):
                        self.answer_NP.append(["LOCATION", "ORGANIZATION",'organization','place'])
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