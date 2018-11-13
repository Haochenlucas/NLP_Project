import os
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
os.environ['JAVAHOME'] = "D:/Java/jdk1.8.0_191/bin" #insert approriate version of jdk
from nltk.tag import StanfordNERTagger

# This is the class to store story instance
class Story:
    # Maybe NER library as well
    def __init__(self, storyFileName):
        # cwd = os.getcwd()
        # storyFile = open(cwd + '/developset/' + storyFileName, encoding='UTF-8')
        storyFile = open(storyFileName, encoding='UTF-8')
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

    def find_tag(self,NP):
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
                is_NER = 0
                if (type(NP) is nltk.tree.Tree and NP._label == 'NP'):
                    for l in range(start,start+len(NP)):
                        if ner_story[i][l][1] != 'O':
                            a = [" ".join(list(list(zip(*NP))[0]))]
                            a.append(ner_story[i][l][1])
                            nerchunk_story[i].append(a)
                            is_NER = 1
                            break
                    if is_NER == 0:
                        word=self.find_tag(NP)
                        nerchunk_story[i].append(word)
                    start += len(NP)
                else:
                    prop = []
                    prop.append(NP[0])
                    prop.append(NP[1])
                    nerchunk_story[i].append(prop)
                    start += 1
        print(nerchunk_story)
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
        # print(NPchunk_tagged)
        return nerchunk_story
    
