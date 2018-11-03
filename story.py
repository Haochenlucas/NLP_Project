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
        namedEnt = []
        for line in self.sent_POS:
            namedEnt.append(nltk.ne_chunk(line, binary=True))

        output = []
        for line in namedEnt:
            for NE in line:
                if(type(NE) is nltk.tree.Tree and NE._label == 'NE'):
                    NP = ""
                    for w in NE:
                        NP += w[0] + " "
                    output.append(NP)
        print(output)
    