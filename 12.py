from nltk.corpus import wordnet as wn
import itertools
def get_similarity_score_1(word,given_list):
    max_similarity=0
    if word.lower() in given_list:
        max_similarity=1
    else:
        current_verb_list=wn.synsets(word.lower())
        for verb in given_list:
            related_verbs=wn.synsets(verb)
            for a,b in itertools.product(related_verbs,current_verb_list):
                if wn.wup_similarity(a,b) == None:
                    d = 0
                else:
                    d=wn.wup_similarity(a,b)
                if d > max_similarity:
                    max_similarity=d
    return max_similarity

print(get_similarity_score_1('run','open'))