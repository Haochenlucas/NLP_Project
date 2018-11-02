import sys
import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

cwd = os.getcwd()
question= open(cwd + '/developset/1999-W02-5.questions', encoding='UTF-8')
question = question.read().splitlines()
n = question.count('')
while n > 0:
    question.remove('')
    n = n - 1
print('After read.splitlines and remove enter:\n',question,'\n')

questionlines = [[] for i in range(len(question))]
for i,sent in enumerate(question):
    questionlines[i] = word_tokenize(sent)
print('After tokenize:\n',questionlines,'\n')
questionlines = questionlines[1:len(questionlines):3]
print('Extract questionlines:\n',questionlines,'\n')

for ques in questionlines:
    for word in ques:
        print(nltk.pos_tag(nltk.word_tokenize(word)))


print ("Get question type")
for ques in questionlines:
    for word in ques:
        word_w_tag = nltk.pos_tag(nltk.word_tokenize(word))
        tag = word_w_tag[0][1]
        if (tag == "WDT" or tag == "WP" or tag == "WP$" or tag == "WRB"):
            print (word_w_tag)