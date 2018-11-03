import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import os

cwd = os.getcwd()
os.environ['JAVAHOME'] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_102.jdk/Contents/Home" #insert approriate version of jdk
# os.environ['JAVAHOME'] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_102.jdk/Contents/Home" #insert approriate version of jdk
from nltk.tag import StanfordNERTagger

question = open(cwd + '/developset/1999-W02-5.questions', encoding='UTF-8')
question = question.read().splitlines()
n = question.count('')
while n > 0:
    question.remove('')
    n = n - 1
print('After read.splitlines and remove enter:\n',question,'\n')

#Tokenize
questionlines = [[] for i in range(len(question))]
for i,sent in enumerate(question):
    questionlines[i] = word_tokenize(sent)
print('After tokenize:\n',questionlines,'\n')
questionlines = questionlines[1:len(questionlines):3]
for ques in questionlines:
    ques.remove('Question')
    ques.remove(':')
print('Extract questionlines:\n',questionlines,'\n')

# Construct bag-of-words for questions
# Remove stop_words
stop_words = set(stopwords.words('english'))
filtered_question = [[] for i in range(len(questionlines))]
for i,ques in enumerate(questionlines):
    for w in ques:
        if w not in stop_words:
            filtered_question[i].append(w)
print('After remove stop_words:\n',filtered_question,'\n')


#NER
eng_tagger = StanfordNERTagger(model_filename=cwd + '/stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
          path_to_jar=cwd + '/stanford-ner-2018-10-16/stanford-ner.jar')
ner_question=[]
for ques in filtered_question:
    ner_question.append(eng_tagger.tag(ques))
print('After NER:\n',ner_question,'\n')