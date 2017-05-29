from dbFuncns import db_funcs as db
from mostProbTopic.implementation import QnA

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


# Takes a question and a state from which querying starts and a boolean (False if it is the first call of the function or false otherwise)
# Returns an answer and a state.
def callback_for_reply(question, state, matchFound):
    subLists = db.get_subtopics(state)
    # print(subLists)
    if len(subLists) == 0:
        return (db.get_data(state), state)

    subTopicsParsed = split_subtopics(subLists)
    singleSubTopicsParsed = flatten_list(subTopicsParsed)
    # print(singleSubTopicsParsed)

    # Send question and a list of topics to Arijit's api call
    # Get back a list of topics and their probabilities in decreasing order as a list of tuples
    mostProbableTopics = QnA(question, singleSubTopicsParsed)

    # sorted(mostProbableTopics,key=lambda x: x[1],reverse = True)

    print(mostProbableTopics)
    probableTopicsForDB = combine_for_querying(mostProbableTopics, subLists)

    threshold = 0.4

    # dataFromCurrentState = get_data(state)

    if probableTopicsForDB[0][1] > threshold:
        return callback_for_reply(question, probableTopicsForDB[0][0], True)
    else:
        if matchFound:
            return ("I suppose you can go to the following subtopics " + " ".join(subLists), state)
        else:
            return ("I didn't get you really !! Please choose something related to " + " ".join(subLists), state)

            # # Think of an algorithm which decides the reply to send
            # for ans in Ans:
            # 	if ans[1] > 0.5:
            # 		callback_for_reply(question, ans[0])
            # 		break;
            # 	elif ans[1] > 0.3:
            # 		callback_for_reply(question, ans[0])
            # 	else:
            # 		callback_for_reply()


# list1 = ["Huzefa", "Harsha/Varsha", "Arijit", "Purav/Sagar","Anusha"]
# prob = [("Anusha", 0.9), ("Varsha", 0.85), ("Sagar", 0.6), ("Purav", 0.5), ("Huzefa", 0.45), ("Harsha", 0.3)]

# print(combine_for_querying(prob,list1))

print(callback_for_reply("What is dangerous?", "Mymanual", False))
print(db.get_parent("Easy-Start"))