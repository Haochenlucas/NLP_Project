from story import Story
from question import Question

# Creat a story object
story = Story("1999-W02-5.story")

# Do things to the story object
s_bags = story.remove_stopwords(story.bags)
s_bags = story.stem_words(s_bags)
# story.pos_tag()
# print(bags)

# Creat a question
question = Question("1999-W02-5.questions")
# Do things to the question object
q_bags = story.remove_stopwords(question.questions)
q_bags = story.stem_words(q_bags)

# Loop all the questions for that story
for x,q in enumerate(q_bags):
    # score of each sentences for a single question
    # should be initialzed to 0 after answering a question
    score = [0]*len(s_bags)
    for i,q_word in enumerate(q):
        for j,s_sent in enumerate(s_bags):
            # Give score for each sentences in the story
            if (q_word in s_sent):
                score[j] += 1
    # Find the match NP in sentence with the highest score

    # O/I the answer
    max_score = max(score)
    best = [i for i, x in enumerate(score) if x == max_score]
    print(question.questiontxt[x])
    for m,a in enumerate(best):
        print("Answer in: " + story.sentences[a])
    print("\n")

# Move on the the next story