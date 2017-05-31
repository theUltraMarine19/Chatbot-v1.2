import random

from CONSTANTS import file_constants
from dbFuncns import db_funcs as db
from mostProbTopic.implementation import QnA

def get_answer():
    return 0

def sent_answer(qn,currrentState):
    print("In sent")
    ans = callback_for_reply(qn, currrentState, file_constants.myConstants.myScoreInit)
    return ans

# Takes a list of topics and returns a list of lists that replaces the topics which have a '/' with
# a list containing the topics in a separate list
def split_subtopics(list):
    return [element.split("/") for element in list]


# Takes a list of lists or normal elements and returns a list containing all the elements in a single list
def flatten_list(list):
    return [item for sublist in list for item in sublist]


# Takes a list of lists and returns a simple list of strings with the sublists replaced by the / concatenated strings
def combine_subtopics(list):
    return ['/'.join(element) for element in list]

# Takes a probList i.e. a list of tuples containing topics and their probs (topics which we wish to be queried) .Is given by the
# QnA function and also a subList which has the list of all the original topics and returns a tuple where each of the
# tuple has the first element that is directly queriable
def combine_for_querying(probList, sublists):
    ## Make two dicts stroing the information whether a particular topic is visited or not.
    vis = {}
    corr = {}
    i = 0
    splittedList = split_subtopics(sublists)
    for el in splittedList:
        if isinstance(el, list):
            for topic in el:
                corr[topic] = i
        else:
            corr[el] = i
        i += 1

    combinedList = []
    for element in probList:
        if not corr[element[0]] in vis:
            combinedList.append((sublists[corr[element[0]]], element[1]))
            vis[corr[element[0]]] = True
    return combinedList

# Takes a question and a state from which querying starts and a score
# Returns an answer,state and a possible score

def callback_for_reply(question, state, myScore):
    subLists = db.get_subtopics(state)
    # print(subLists)

    maxMsg = ""
    maxState = ""
    maxScore = file_constants.myConstants.maxScoreInit

    if len(subLists) == 0:
        return (db.get_data(state), file_constants.myConstants.initialState, myScore)

    subTopicsParsed = split_subtopics(subLists)
    singleSubTopicsParsed = flatten_list(subTopicsParsed)
    # print(singleSubTopicsParsed)

    # Send question and a list of topics to Arijit's api call
    # Get back a list of topics and their probabilities in decreasing order as a list of tuples
    print("In callback before QnA")
    mostProbableTopics = QnA(question, singleSubTopicsParsed)
    print(mostProbableTopics)
    print("In callback after QnA")

    # sorted(mostProbableTopics,key=lambda x: x[1],reverse = True)

    #print(mostProbableTopics)
    probableTopicsForDB = combine_for_querying(mostProbableTopics, subLists)

    thresholdLow  = 0.4
    thresholdHigh = 0.6

    # dataFromCurrentState = get_data(state)

    for i in range(0,len(probableTopicsForDB)):
        msg, st, score = callback_for_reply(question, probableTopicsForDB[i][0], probableTopicsForDB[i][1])
        if score > thresholdLow:
            if score > thresholdHigh:
                return (msg, st, score)
            elif score> myScore:
                maxMsg = msg
                maxState = st
                maxScore = score
        else:
            str10 = "I suppose you can go to the following subtopics: \n"
            str11 = "Do you want to know more about any of the following: \n"
            str12 = "Am almost able to find your answer. Tell me whether you want one of the following: \n"
            str13 = "I need more help :( Please select one of the following: \n"
            str3 = [str10, str11, str12, str13]

            ind = random.randint(0, 3)
            str1 = str3[ind]
            str2 = ""

            listmsg = ""

            for ele in subLists:
                listmsg += "\t" + ele + "\n"
                str2 = "I didn't get you really !! Please choose something related to: \n"

            if maxScore == file_constants.myConstants.maxScoreInit :
               if myScore == file_constants.myConstants.myScoreInit:
                   return (str2+listmsg, state,myScore)
               else:
                   return (str1 + listmsg, state, myScore)
            else:
                return(maxMsg, maxState, maxScore)
                # if myScore != -1:
                #     #return ("I suppose you can go to the following subtopics " + '\n'.join(subLists), state)
                #     return (str1+listmsg, state)
                # else:
                #     #return ("I didn't get you really !! Please choose something related to " + " ".join(subLists), state)
                #     return (str2 + listmsg, state)
    return(maxMsg, maxState, maxScore)

# replyMsg,state,score = callback_for_reply("What is dangerous?", file_constants.myConstants.initialState, file_constants.myConstants.myScoreInit)
# print(replyMsg)
# replyMsg,state, score = callback_for_reply("Do you think the safety is enough for children?", "Mymanual", file_constants.myConstants.myScoreInit)
# print(replyMsg)
# replyMsg, state, score = callback_for_reply("How to activate Easy-Start on my toothbrush?", "Mymanual", file_constants.myConstants.myScoreInit)
# print(replyMsg)
# replyMsg, state, score = callback_for_reply("What are the different parts of my toothbrush?", "Mymanual", file_constants.myConstants.myScoreInit)
# print(replyMsg)
# replyMsg, state, score = callback_for_reply("What are the different modes of using the toothbrush?", "Mymanual", file_constants.myConstants.myScoreInit)
# print(replyMsg)
# replyMsg, state, score = callback_for_reply("Can it be used for commercial use?", "Mymanual", file_constants.myConstants.myScoreInit)
# print(replyMsg)
# replyMsg, state, score = callback_for_reply("What is the cost?", "Mymanual", file_constants.myConstants.myScoreInit)
# print(replyMsg)
# replyMsg, state, score = callback_for_reply("Is the toothbrush safe?", "Mymanual", file_constants.myConstants.myScoreInit)
# print(replyMsg)
# replyMsg,state, score = callback_for_reply("What is dangerous?", "Mymanual", file_constants.myConstants.myScoreInit)
# print(replyMsg)