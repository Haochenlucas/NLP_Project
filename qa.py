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
                if (NE[-1] in question.answer_NP[i]):
                    answer.append(NE[0])
    return answer

def filter_NE_Chuck(NE_chuck):
    badword = ["who"]
    for sents in NE_chuck:
        for chuck in sents:
            if(chuck[0] in badword):
                chuck[1] = "none"

# def word_match(score, Q_chuck, scored_chuck):
#     # Give score for each sentences in the story
#     scored = False
#     # Mark the chuck as scored and not add score again if any word in chuck shows up
#     # print(NE_Q_chuck)
#     for chuck in Q_chuck[x]:
#         if (q_NP in chuck):
#             chuck_i = Q_chuck[x].index(chuck)
#             if (chuck_i not in scored_chuck):
#                 score[j] += 1
#                 scored = True
#                 scored_chuck.append(chuck_i)
#                 break
#     if(not scored):
#         score[j] += 1
#     return score

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
    s_bags = story.stem_words(s_bags)
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
    q_bags = story.stem_words(q_bags)
    # print(q_bags)

    # Loop all the questions for that story
    # for x,q in enumerate(q_bags):
    #     # Scoring system:
    #     # 1. Check question type and only analize sentences that contain the right type of NE
    #     # 2. Matching NP form Q with sentences in S
    #     # score of each sentences for a single question
    #     # should be initialzed to 0 after answering a question
    #     score = [0]*len(s_bags)
    #     for j,s_sent in enumerate(s_bags):
    #         # +1 for each NP with the matching Q type and not in the Q
    #         # match_type(score, NE_S_chuck[j], NE_Q_chuck[x], question.answer_NP[x], j)
    #         scored_chuck = []
    #         for i,q_NP in enumerate(q):
    #             # Give score for each sentences in the story
    #             if (q_NP in s_sent):
    #                 # +1 for each matching NP
    #                 score = word_match(score, Q_chuck, scored_chuck)
    #     print(score)
    #     # print all the sentences that might have the answers



    # BASIC_RULE WordMatch
    score_table=[]
    for q_sent in NE_Q_chuck:
        score = []
        for s_sent in NE_S_chuck:
            s_score = 0
            for word in s_sent:
                if word[0] in list(list(zip(*q_sent))[0]):
                    if word[0] in stopWords:
                        s_score += 0
                    else:
                        s_score += 1
                else:
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
                                        s_score += max_similarity
            score.append(s_score)
        score_table.append(score)
    print(score_table)

    for i,q_sent in enumerate(NE_Q_chuck):
        # # VB score
        # for word in q_sent:
        #     if re.match("VB\w+", word[1]):
        #         if wordnet.synsets(word[0]):
        #             for j, s_sent in enumerate(NE_S_chuck):
        #                 for w in s_sent:
        #                     if re.match("VB\w+", w[1]):
        #                         if wordnet.synsets(w[0]):
        #                             max_similarity = 0
        #                             for a, b in itertools.product(wordnet.synsets(w[0]), wordnet.synsets(word[0])):
        #                                 if wordnet.wup_similarity(a, b) == None:
        #                                     d = 0
        #                                 else:
        #                                     d = wordnet.wup_similarity(a, b)
        #                                 if d > max_similarity:
        #                                     max_similarity = d
        #                             if max_similarity > 0.66:
        #                                 score_table[i][j] += 1
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
                    if(("DATE" in tags) or ("TIME" in tags) or ("period" in tags)):
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
        print("\n")
        for m, a in enumerate(answer):
            if (a != ""):
                if(a not in list(list(zip(*NE_Q_chuck[i]))[0])):
                    print("Answer: " + answer[m])

        print("\n")