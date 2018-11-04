import sys
import os
import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import wordnet as wn
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

os.environ['JAVAHOME'] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_102.jdk/Contents/Home" #insert approriate version of jdk
from nltk.tag import StanfordNERTagger

# This is the class to store story instance
class Story:
    # Maybe NER library as well
    def __init__(self, storyFileName):
        cwd = os.getcwd()
        storyFile = open(cwd + '/developset/' + storyFileName, encoding='UTF-8')
        self.story = storyFile.read()
        storyFile.close()
        self.story = self.story.replace('\n',' ')
        cut = 'STORYID: '
        id_and_text = self.story.split(cut, 1)[1]
        cut = 'TEXT: '
        self.storyID = id_and_text.split(cut, 1)[0]
        self.story = id_and_text.split(cut, 1)[1]
        self.sentences = sent_tokenize(self.story)
        self.bags = [[] for i in range(len(self.sentences))]
        # word tokenize for sentences
        self.sent_POS = []
        for i,sent in enumerate(self.sentences):
            self.bags[i] = word_tokenize(sent)

    # remove stop words
    def remove_stopwords(self, wordbags):
        stopsWords = set(stopwords.words('english'))
        # print(stopsWords)
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

    def print_sents(self):
        print(self.sentences)
    
    # Grouping NE
    def chuck_NE(self):
        grammar = r"""  
                NP: {<DT>?(<JJ>* <NN.*>)? <JJ>* <NN.*>+}
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
        # print('The NP chunk\n',np_chunk,'\n')

        # cwd = os.getcwd()
        # eng_tagger = StanfordNERTagger(model_filename=cwd + '/stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
        #         path_to_jar=cwd + '/stanford-ner-2018-10-16/stanford-ner.jar')
        # ne_story=[[]for i in range(len(np_chunk))]
        # for i,NP in enumerate(np_chunk):
        #     set=[]
        #     for w in NP:
        #         words = nltk.word_tokenize(w)
        #         s = eng_tagger.tag(words)
        #         for w in s:
        #             if w[1] != 'O':
        #                 print(s,w[1])
        #                 break
    
