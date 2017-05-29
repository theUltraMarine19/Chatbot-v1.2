import sys
# from PorterStemmer import *
# from wordparser import *
# from vectorspace import *
#
# e = PorterStemmer()
# # v = VectorSpace(["cat","cat dog","hat"],[])
# # li = v.search(["cat","hat"])
# # print(li)
# # v1 = VectorSpace(["cat","cat dog","hat"])
# # l2 = v1.related(0)
# # print(l2)
# # k = v.get_vector_keyword_index(['Do you know to restarts Sonicare','How do I start Sonicare'])
# # #print(k)
# # #v.build(['Do you know to restarts Sonicare','How do I start Sonicare'],None)
# # # for keys, values in k.items():
# # #     print(keys)
# # #     print(values)
# # word = 'connected'
# # res = e.stem(word,0,len(word)-1)
# #print(res)
# p = Parser()
# result = p.tokenise_and_remove_stop_words(['Do you know to restarts Sonicare?'])
# print(result)
# #print(p.stopwords)

def QnA(qn,tl):
    from mostProbTopic.test import Test
    from mostProbTopic.wordparser import Parser
    #
    # docs = ["Human machine interface for lab abc computer applications",
    #         "A survey of user opinion of computer system response time",
    #         "The EPS user interface management system",
    #         "System and human system engineering testing of EPS",
    #         "Relation of user perceived response time to error measurement",
    #         "The generation of random binary unordered trees",
    #         "The intersection graph of paths in trees",
    #         "Graph minors IV Widths of trees and well quasi ordering",
    #         "Graph minors A survey"]

    # docs = ['Parts', 'Components', 'Away from water', 'Dry', 'Voltage', 'Damaged', 'Broken', 'Outdoor usage', 'Supervised usage', 'children', 'mentally challenged', 'Surgery', 'Consulting Dentist', 'Electromagnetic Impact', 'Pacemaker', 'Alternative', 'Different Uses', 'Discomfort', 'Pain', 'Commercial Use', 'Other Manufacturer', 'Replace', 'Renew', 'Cleaning', 'Toothpaste', 'Brush head', 'Collective', 'All Dangers', 'Safety Measures', 'Dangers', 'Warnings', 'Scrub', 'Motion', 'Pressure', 'Collective', 'How to Best Use Brush', 'Techniques to Use Brush', 'Quadpacer', 'Beeper', 'Info about Modes', 'Clean', 'White', 'Polish', 'Gum care', 'Sensitive', 'Modes', 'Modes', 'Ways to Use', 'Quadpacer', 'Info', ' About Easy-start', 'Activate', 'Enable', 'Start', 'Deactivate', 'Disable', 'Stop', 'Easy-Start', 'Info', 'About Charging', 'Wall socket', 'USB', 'Charging', 'Battery', 'Cleaning', 'Rinse', 'Wash', 'Store', 'Keep Aside', 'Cleaning', 'Maintenance', 'Rinse', 'Wash', 'Storing', 'Info', 'Model', 'Battery Removal', 'Disposal', 'Throw Away', 'Trash', 'Service', 'Care Center', 'Warranty', 'Guarantee', 'Issues', 'Problems', 'Doesn’t Work', ' Doesn’t Start', 'Issues', 'Problems', 'Warranty', 'Guarantee', 'Service', 'Doesn’t Work']
    docs = tl
    docs = list(set(docs))
    ## Avoid entering only one doc in the doc list
    # print(len(docs))
    t = Test(docs)
    p = Parser()
    result = p.tokenise_and_remove_stop_words(['safety'])
    # print(result)
    q = t.input('How to easy-start my Sonicare brush?')  # Isn't working
    q1 = t.input('How do I repairing my mixer?')
    q2 = t.input('handle with ergonomic shape')
    q3 = t.input("Please help me with charging")
    q4 = t.input("Is it safe for children?")
    question = t.input(qn)
    # print('How to easy-start my Sonicare brush?'+"Please help me with charging")
    q = t.input('How to easy-start my Sonicare?')
    q = t.inputs('How to easy-start my Sonicare brush?'+" Please help me with charging")
    res = t.get_doc(question)
    #print(res)
    return res