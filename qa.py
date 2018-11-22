from story import Story
from question import Question
from nltk.corpus import stopwords
import re
from nltk.corpus import wordnet
import itertools
# Functions:
def find_answer(best, question,i):
    answer = []
    for sent_idx in best:
            for NE in NE_S_chuck[sent_idx]:
                if(question.questions[i][0].lower() == "why"):
                    HERE = 0
                elif (NE[-1] in question.answer_NP[i]):
                    answer.append(NE[0])
    return answer

def filter_NE_Chuck(NE_chuck):
    badword = ["who"]
    for sents in NE_chuck:
        for chuck in sents:
            if(chuck[0] in badword):
                chuck[1] = "none"

# NE_S_chuck: NE chuck for sentence i of the story
# NE_Q_chuck: NE chuck for sentence j of the sentence
# def match_type(score, NE_S_chuck, NE_Q_chuck, questionType):
#     for NE in NE_S_chuck:
#         print(NE)
#         if (NE not in NE_Q_chuck and NE[-1] in questionType):
#             score[j] += 1
#     return score

# cwd = os.getcwd()
# for file in os.listdir(cwd + '/developset'):
#     if file.endswith(".story"):
        # instance = file[:-6]

input = open('input.txt')
path = input.readline()
path = path.replace('\n','')
instances = []
line = input.readline()
line = line.replace('\n','')
stopWords = set(stopwords.words('english'))
print(stopWords)
while (line):
    instances.append(line)
    line = input.readline()
    line = line.replace('\n','')

for foldname in instances: 
    # reponsefile = open("reponsefile.txt","w")
    # Creat a story object
    # story = Story(instance + ".story")
    # story = Story("1999-W02-5.story")
    story = Story(path +'/' + foldname + '/' + foldname + ".story")
    s_bags = story.pos_tag(story.bags)
    # Do things to the story object
    NE_S_chuck = story.chuck_NE()
    filter_NE_Chuck(NE_S_chuck)
    s_bags = story.remove_stopwords(story.bags)
    # s_bags = story.stem_words(s_bags)
    # print(s_bags)

    # Creat a question
    # question = Question(instance + ".questions")
    # question = Question("1999-W02-5.questions")
    # Do things to the question object
    # Q_chuck = question.chuck_NP()
    question = Question(path + '/'+foldname + '/' + foldname + ".questions")
    q_bags = question.pos_tag(question.questions)
    question.answer_NP_type()
    Q_chuck = question.chuck_NP()
    NE_Q_chuck = question.NER()
    q_bags = story.remove_stopwords(question.questions)
    # q_bags = story.stem_words(q_bags)
    # print(q_bags)


    # BASIC_RULE WordMatch
    score_table=[]
    for x,q_sent in enumerate(NE_Q_chuck):
        score = []
        q_NE = list(list(zip(*q_sent))[0])
        q_NE_lower = [i.lower() for i in q_NE]
        q_words_lower = [i.lower() for i in q_bags[x]]
        for s_sent in NE_S_chuck:
            s_score = 0
            scored_Schunck = []
            for word in s_sent:
                notFound = True
                for w in word[0].split():
                    if w in q_words_lower:
                        notFound = True
                        if w in stopWords:
                            s_score += 0
                        else:
                            scored = False
                            scored_Qchuck = []
                            # Mark the chuck as scored and not add score again if any word in chuck shows up
                            # print(NE_Q_chuck)
                            for chuck in q_NE_lower:
                                if (w in chuck):
                                    notFound = False
                                    chuck_i = q_NE_lower.index(chuck)
                                    if (chuck_i not in scored_Qchuck and w not in scored_Schunck):
                                        s_score += 1
                                        scored = True
                                        scored_Schunck.append(w)
                                        scored_Qchuck.append(chuck_i)
                                        break
                            if(not scored and w not in scored_Schunck):
                                s_score += 1
                                scored_Schunck.append(w)

                if(notFound):
                    if wordnet.synsets(word[0]):
                        for qword in q_sent:
                            if wordnet.synsets(qword[0]):
                                max_similarity = 0
                                if word[0] not in stopWords and qword[0] not in stopWords:
                                    for a, b in itertools.product(wordnet.synsets(qword[0]), wordnet.synsets(word[0])):
                                        if wordnet.wup_similarity(a, b) == None:
                                            d = 0
                                        else:
                                            d = wordnet.wup_similarity(a, b)
# overlap(gloss(w1),gloss(w2)) +
# overlap(gloss(hypo(w1),hypo(w2))) +
# overlap(gloss(w1),gloss(hypo(w1))) +
# overlap(gloss(hypo(w1)),gloss(w2)))
                                        if d > max_similarity:
                                            max_similarity = d
                                    if max_similarity > 0.66:
                                        s_score += round(max_similarity, 2)
            score.append(s_score)
        score_table.append(score)
    print(score_table)

    for i,q_sent in enumerate(NE_Q_chuck):
        prop = list(list(zip(*q_sent))[1])
        for word in q_sent:
            # who rules:
            if(word[0].lower() == "who"):
                if 'PERSON' not in prop and 'ORGANIZATION'not in prop:
                    for j,s_sent in enumerate(NE_S_chuck):
                        if 'PERSON' in list(list(zip(*s_sent))[1]):
                            score_table[i][j] += 6
                        elif 'name' in list(list(zip(*s_sent))[0]):
                            score_table[i][j] += 4
                    for j, s_sent in enumerate(NE_S_chuck):
                        if  'preson' in list(list(zip(*s_sent))[1]):
                            score_table[i][j] += 4
                # else:
                #     for j, s_sent in enumerate(NE_S_chuck):
                #         if 'preson' in list(list(zip(*s_sent))[1]):
                #             score_table[i][j] += 6
                #         if 'organization' in list(list(zip(*s_sent))[1]):
                #             score_table[i][j] += 6

            elif(word[0].lower() == "where"):
                for j, sent in enumerate(NE_S_chuck):
                    tags = list(list(zip(*sent))[1])
                    if(('LOCATION' in tags) or ('place' in tags) or ('ORGANIZATION' in tags) or ('organization' in tags)):
                        score_table[i][j] += 6

            elif(word[0].lower() == "when"):
                for j, sent in enumerate(NE_S_chuck):
                    tags = list(list(zip(*sent))[1])
                    if(("DATE" in tags) or ("time" in tags) or ("period" in tags)):
                        score_table[i][j] += 4
                    if(("start" in q_sent or "begin" in q_sent) and ("start" in tags or "begin" in tags or "since" in tags or "year" in tags)):
                        score_table[i][j] += 20

    print(score_table)
    # O/I the answer
    for i,score in enumerate(score_table):
        max_score = max(score)
        print(question.questiontxt[i])
        best = [i for i, x in enumerate(score) if x == max_score]
        for m, a in enumerate(best):
            print("Answer: " + story.sentences[a])
        answer = find_answer(best, question,i)
        
        answerout = ""
        for m, a in enumerate(answer):
            if (a != ""):
                if(a not in list(list(zip(*NE_Q_chuck[i]))[0])):
                    answerout += answer[m] + "/ "
        print("Answer: " + answerout, end="")
        print("\n")