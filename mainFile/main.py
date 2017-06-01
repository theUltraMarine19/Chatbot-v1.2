import random

from CONSTANTS import file_constants
from dbFuncns import db_funcs as db
from mostProbTopic.implementation import QnA


def sent_answer(qn,currrentState):
    ans = callback_for_reply(qn, currrentState, file_constants.myConstants.myScoreInit)
    fp = open("questions.txt","a+")
    fp.write("question:"+qn+"\n")
    fp.write("answer:"+ans[0]+"\n")
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
    ## Make two dicts storing the information whether a particular topic is visited or not.
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

str_1 = "I suppose you can go to the following subtopics: \n"
str_2 = "Do you want to know more about any of the following: \n"
str_3 = "Am almost able to find your answer. Tell me whether you want one of the following: \n"
str_4 = "I need more help to get you your answer:( Please select one of the following: \n"
strOptsForStuckState = [str_1, str_2, str_3, str_4]
strInitStateReply = "I didn't get you really !! Please choose something related to: \n"

# Takes a question and a state from which querying starts and a score
# Returns an answer,state and a possible score
def callback_for_reply(question, state, myScore):
    global strOptsForStuckState, strInitStateReply
    subLists = db.get_subtopics(state)

    maxMsg = ""
    maxState = ""
    maxScore = file_constants.myConstants.maxScoreInit

    if len(subLists) == 0:
        # returns data at the leaf
        return (db.get_data(state), file_constants.myConstants.initialState, myScore)

    subTopicsParsed = split_subtopics(subLists)
    singleSubTopicsParsed = flatten_list(subTopicsParsed)

    # Send question and a list of topics to QnA api call from mostProbTopic
    # Get back a list of topics and their probabilities in decreasing order as a list of tuples
    mostProbableTopics = QnA(question, singleSubTopicsParsed)
    # print(mostProbableTopics)

    probableTopicsForDB = combine_for_querying(mostProbableTopics, subLists)

    thresholdLow  = file_constants.myConstants.thresholdLow
    thresholdHigh = file_constants.myConstants.thresholdHigh

    # dataFromCurrentState = get_data(state)

    for i in range(0,len(probableTopicsForDB)):
        msg, st, score = callback_for_reply(question, probableTopicsForDB[i][0], probableTopicsForDB[i][1])
        if score > thresholdLow:
            if score > thresholdHigh:
                return (msg, st, score)
            elif score> maxScore:
                maxMsg = msg
                maxState = st
                maxScore = score
        else:

            subTopicsListReply = ""
            for subListName in subLists:
                subTopicsListReply += "\t" + subListName + "\n"

            if maxScore == file_constants.myConstants.maxScoreInit :
               if myScore == file_constants.myConstants.myScoreInit:
                   return (strInitStateReply+subTopicsListReply, state,myScore)
               else:
                   ind = random.randint(0, 3)
                   str_for_reply = strOptsForStuckState[ind]
                   return (str_for_reply + subTopicsListReply, state, myScore)
            else:
                return(maxMsg, maxState, maxScore)

    return(maxMsg, maxState, maxScore)