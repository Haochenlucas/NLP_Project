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
        for i,sent in enumerate(self.sentences):
            self.bags[i] = word_tokenize(sent)

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

    # # tage NP in the Story
    # def ner_tagging(sent):
    #     return

    def print_sents(self):
        print(self.sentences)
    