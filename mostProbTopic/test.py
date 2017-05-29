from mostProbTopic.vectorspace import VectorSpace
import nltk
import math
from nltk.stem.porter import *
stemmer = PorterStemmer()
import nltk.data
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


class Test:

    def __init__(self,doc_list):
        self.documents = doc_list

    def get_doc(self,keyword_list):
        v = VectorSpace(self.documents)
        # print("HERE \n % s" % keyword_list)
        li = v.search(keyword_list)
        # print(li)
        ctr = 0
        for item in li:
            # print(item)
            if math.isnan(item):  # Robust checking needed
                li[ctr] = -1.0
            ctr += 1    
        # li.sort(reverse=True)
        # print("THE LIST %s" % li)
        # pl = sorted(range(len(li)), key=lambda x: li[x])[-5:]
        pl = sorted(range(len(li)), key=lambda x: li[x], reverse = True) # Sorting
        # print(pl)
        # pl.sort(reverse=True)
        # print("THE QUERY WEIGHTS %s" % li) 
        # LET'S SORT li AND TRY
        # sorted(pl,key=lambda y: li[y],reverse=True) # Are you double sorting it?
        maxl = max(li)
        # print("\n")
        # print(pl)
        # print(maxl)
        result = []
        # if maxl == 2:
        #     return "Sorry! I am not aware of that."
        max_index = li.index(maxl)
        for index in pl:
            tuple = ()  # making the tuple
            # print(self.documents[index])
            # print(li[index])
            tuple = (self.documents[index],li[index])
            # print(tuple)
            result.append(tuple)
        return result

    def input(self,question): # single intent question in one turn
        v = VectorSpace()
        p = v.parser
        # qs = nltk.sent_tokenize(questions)
        words = nltk.word_tokenize(question)
        tagged = nltk.pos_tag(words)
        # for word in tagged:
        #     print(word[1])
        result = p.tokenise_and_remove_stop_words([question])
        intent = []
        for word in tagged:
            if stemmer.stem(word[0]) in result:
                if word[1] in ['VB','VBD','VBG','VBN','VBP','VBZ']:
                    intent.append(stemmer.stem(word[0]))
        # print(intent)
        # print(nltk.pos_tag(result))
        return [question]


    def inputs(self,questions): # Handle multiple questions (multi-intended) in one turn
        qs = tokenizer.tokenize(questions)
        # print(qs)
        lq = []
        for question in qs:
            lq.append(self.input(question))
        # print(lq)
        return lq


