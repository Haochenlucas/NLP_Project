import sys
import os
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


cwd = os.getcwd()
story = open(cwd + '/developset/1999-W02-5/1999-W02-5.story', encoding='UTF-8')
story = story.read()
story = story.replace('\n',' ')
sep = 'TEXT: '
rest = story.split(sep, 1)[1]
storylines = sent_tokenize(story)
print(storylines)
dictlines = [[] for i in range(storylines.__len__())]
for i,sent in enumerate(storylines):
    dictlines[i]=word_tokenize(sent)
# print(dictlines)
# POS
pos_story=[]
for i,ques in enumerate(dictlines):
    dictlines = ' '.join(ques)
    tokens = nltk.word_tokenize(dictlines)
    pos = nltk.pos_tag(tokens)
    pos_story.append(pos)
print('After POS\n',pos_story,'\n')

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
bags = [[] for i in range(len(pos_story))]
cp = nltk.RegexpParser(grammar)
tree_S = []
for i, pos in enumerate(pos_story):
    tree_S.append(cp.parse(pos))

def find_tag(NP):
    catg = list(list(zip(*NP))[1])
    word = list(list(zip(*NP))[0])
    if any(i =='$'for i in (catg)):
        word.append('MONEY')
    else:
        suspect = word[-1].lower()
        if not wordnet.synsets(suspect):
            #print('Not an English Word')
            word.append('none')
        else:
            print(suspect)
            suspect = wordnet.synsets(suspect)[0]
            typelist = ['period', 'organization', 'cost','person','place']
            max = [0.55,'none']
            for ele in typelist:
                type = wordnet.synsets(ele)[0]
                value=0
                if type.wup_similarity(suspect)==None:
                    value=0
                else:
                    value=type.wup_similarity(suspect)
                if max[0] < value:
                    max[0] = value
                    max[1] = ele
            word.append(max[1])
    print(word)


for trees in tree_S:
    for NP in trees:
        if type(NP) is nltk.tree.Tree and NP._label == 'NP':
            print(NP)
            find_tag(NP)












# STEMMING
# print("after stemming")
# ps = PorterStemmer()
# for line in dictlines:
#     for sent in line:
#         print(ps.stem(sent))

# # Remove stop words
# print("Filtering stop words")
# stopsWords = set(stopwords.words('english'))
# # print(stopsWords)
# wordsFiltered = []
# for line in dictlines:
#     for w in line:
#         if w not in stopsWords:
#             # This "w" here needs to be case insenstive
#             wordsFiltered.append(w)
#
# print(wordsFiltered)

# for line in dictlines:
#     for sent in line:
#         print(nltk.pos_tag(nltk.word_tokenize(sent)))

# os.environ['JAVAHOME'] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_102.jdk/Contents/Home" #insert approriate version of jdk
# from nltk.tag import StanfordNERTagger
# #NER
# eng_tagger = StanfordNERTagger(model_filename=cwd + '/stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
#           path_to_jar=cwd + '/stanford-ner-2018-10-16/stanford-ner.jar')
# ner_question=[]
# ner_question.append(eng_tagger.tag(wordsFiltered))
# print('After NER:\n',ner_question,'\n')