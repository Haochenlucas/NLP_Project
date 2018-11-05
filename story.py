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
        # Find all NP that matches our grammar and put those in trees
        grammar = r"""
        NP: {<DT>?(<JJ>* <NN.*>)? <JJ>* <NN.*>+}
        """
        cp = nltk.RegexpParser(grammar)
        tree_S = []
        for i, ques in enumerate(self.sent_POS):
            tree_S.append(cp.parse(ques))

        # Use Stanfore NER to tag the all the words in the story
        ner_story =[[]for i in range(len(self.bags))]
        cwd = os.getcwd()
        eng_tagger = StanfordNERTagger(model_filename=cwd + '/stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
                path_to_jar=cwd + '/stanford-ner-2018-10-16/stanford-ner.jar')
        for i,sent in enumerate(self.bags):
            ner_story[i] = eng_tagger.tag(sent)

        # Put NE tag on the trees
        nerchunk_story=[[]for i in range(len(self.bags))]
        for i, line in enumerate(tree_S):
            start=0
            for j,NP in enumerate(line):
                if (type(NP) is nltk.tree.Tree and NP._label == 'NP'):
                    for l in range(start,start+len(NP)):
                        if ner_story[i][l][1] != 'O':
                            nerchunk_story[i].append(NP)
                            nerchunk_story[i].append(ner_story[i][l][1])
                            break
                    start += len(NP)
                else:
                    start += 1

        # Normalize out put of all marked NE
        NPchunk_tagged = [[]for i in range(len(nerchunk_story))]
        for k,sent in enumerate(nerchunk_story):
            for i,parse in  enumerate(sent):
                if (type(parse)==nltk.tree.Tree):
                    leaf = parse.leaves()
                    set = []
                    for j,w in enumerate(leaf):
                        set.append(w[0])
                    set.append(nerchunk_story[k][i + 1])
                    NPchunk_tagged[k].append(set)
        return NPchunk_tagged
    
