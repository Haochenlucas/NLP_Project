from story import Story
from question import Question
import os

# Functions:

def find_answer(best, question):
    temp = 1
    for sent_idx in best:
            for NE in NE_S_chuck[sent_idx]:
                if (NE[-1] in question.answer_NP[x]):
                    return " ".join(NE[0:-1])
    return ""


cwd = os.getcwd()
for file in os.listdir(cwd + '/developset'):
    if file.endswith(".story"):
        instance = file[:-6]

# Creat a story object
# story = Story(instance + ".story")
story = Story("1999-W07-2.story")
# Do things to the story object
s_bags = story.pos_tag(story.bags)
NE_S_chuck = story.chuck_NE()
s_bags = story.remove_stopwords(story.bags)
s_bags = story.stem_words(s_bags)
# print(s_bags)

# Creat a question
# question = Question(instance + ".questions")
question = Question("1999-W07-2.questions")
# Do things to the question object
q_bags = question.pos_tag(question.questions)
NE_Q_chuck = question.chuck_NE()
question.answer_NP_type()
q_bags = story.remove_stopwords(question.questions)
q_bags = story.stem_words(q_bags)
# print(q_bags)

# Loop all the questions for that story
for x,q in enumerate(q_bags):

    # Scoring system:
    # 1. Check question type and only analize sentences that contain the right type of NE
    # 2. Matching NP form Q with sentences in S

    # score of each sentences for a single question
    # should be initialzed to 0 after answering a question
    score = [0]*len(s_bags)
    for j,s_sent in enumerate(s_bags):
        scored_chuck = []
        for i,q_NP in enumerate(q):
            # Give score for each sentences in the story
            if (q_NP in s_sent):
                scored = False
                # Mark the chuck as scored and not add score again if any word in chuck shows up
                for chuck in NE_Q_chuck[x]:
                    if (q_NP in chuck.lower()):
                        chuck_i = NE_Q_chuck[x].index(chuck)
                        if (chuck_i not in scored_chuck):
                            score[j] += 1
                            scored = True
                            scored_chuck.append(chuck_i)
                            break
                if(not score):
                    score[j] += 1

    # print all the sentences that might have the answers
    max_score = max(score)
    best = [i for i, x in enumerate(score) if x == max_score]
    # O/I the answer
    print("QuestionID:",question.questionsID[x])
    # print(question.questiontxt[x])

    # Find the match NP in sentence with the highest score

    answer = find_answer(best, question)
    if (answer != ""):
        print("Answer: " + answer,'\n')
    else:
       print("Answer: " + story.sentences[best[0]],'\n')
    # print("\n")

