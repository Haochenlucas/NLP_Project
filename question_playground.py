import sys
import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet

cwd = os.getcwd()
question= open(cwd + '/developset/1999-W02-5/1999-W02-5.questions', encoding='UTF-8')
question = question.read().splitlines()
n = question.count('')
while n > 0:
    question.remove('')
    n = n - 1
# print('After read.splitlines and remove enter:\n',question,'\n')

questionlines = [[] for i in range(len(question))]
for i,sent in enumerate(question):
    questionlines[i] = word_tokenize(sent)
# print('After tokenize:\n',questionlines,'\n')
questionlines = questionlines[1:len(questionlines):3]
for i in questionlines:
    i.remove(i[0])
    i.remove(i[0])
print('Extract questionlines:\n',questionlines,'\n')

print ("Get question type")
for ques in questionlines:
    for word in ques:
        word_w_tag = nltk.pos_tag(nltk.word_tokenize(word))
        tag = word_w_tag[0][1]
        if (tag == "WDT" or tag == "WP" or tag == "WP$" or tag == "WRB"):
            print (word_w_tag)
print('\n')
# POS
pos_question=[]
for i,ques in enumerate(questionlines):
    questionlines = ' '.join(ques)
    tokens = nltk.word_tokenize(questionlines)
    pos = nltk.pos_tag(tokens)
    pos_question.append(pos)
print('After POS\n',pos_question,'\n')

# for ques in pos_question:
#     namedEnt = nltk.ne_chunk(pos_question[0], binary=True )
#     namedEnt.draw()
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
bags = [[] for i in range(len(questionlines))]
cp = nltk.RegexpParser(grammar)
tree_S = []
for i, ques in enumerate(pos_question):
    tree_S.append(cp.parse(ques))


def find_tag(NP):
    catg = list(list(zip(*NP))[1])
    word = list(list(zip(*NP))[0])
    if all(i =='NNP'for i in (catg)):
        word.append('PERSON')
    else:
        suspect = word[-1].lower()
        if not wordnet.synsets(suspect):
            #print('Not an English Word')
            word.append('none')
        else:
            suspect = wordnet.synsets(suspect)[0]
            typelist = ['period', 'organization', 'money','person','place']
            max = [0.55,'none']
            for ele in typelist:
                type = wordnet.synsets(ele)[0]
                if max[0] < type.wup_similarity(suspect):
                    max[0] = type.wup_similarity(suspect)
                    max[1] = ele
            word.append(max[1])
    print(word)



for trees in tree_S:
    for NP in trees:
        if type(NP) is nltk.tree.Tree and NP._label == 'NP':
            find_tag(NP)




# Use Stanfore NER to tag the all the words in the story
# ner_story =[[]for i in range(len(bags))]
# cwd = os.getcwd()
# eng_tagger = StanfordNERTagger(model_filename=cwd + '/stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
#         path_to_jar=cwd + '/stanford-ner-2018-10-16/stanford-ner.jar')
# for i,sent in enumerate(self.bags):
#     ner_story[i] = eng_tagger.tag(sent)

# Put NE tag on the trees
# nerchunk_story=[[]for i in range(len(self.bags))]
# for i, line in enumerate(tree_S):
#     start=0
#     for j,NP in enumerate(line):
#         if (type(NP) is nltk.tree.Tree and NP._label == 'NP'):
#             for l in range(start,start+len(NP)):
#                 if ner_story[i][l][1] != 'O':
#                     nerchunk_story[i].append(NP)
#                     nerchunk_story[i].append(ner_story[i][l][1])
#                     break
#             start += len(NP)
#         else:
#             start += 1
#
# # Normalize out put of all marked NE
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







# for i, line in enumerate(tree_ques):
#     for NP in line:
#         if (type(NP) is nltk.tree.Tree and NP._label == 'NP'):
#             np_tree[i].append(NP)
# print(np_tree)
# for i, NP in enumerate(np_tree):
#     for j, subNP in enumerate(NP):
#         set = []
#         for w in subNP:
#             set.append(w[0])
#         s = ' '.join(set)
#         np_chunk[i].append(s)
# print(np_chunk)
