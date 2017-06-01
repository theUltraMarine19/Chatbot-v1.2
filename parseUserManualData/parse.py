import sys
# sys.path.append('../')

import xml.etree.ElementTree as ET

import nltk

from dbFuncns import db_funcs

fileName = "mymanual"
filePath = "../userManualData"

# Given an attribute find's the corresponding attribute value of the node
def findSecAttribute(par,attribute):
    reqAttributeData = ""
    for child in par :
        if child.tag == attribute :
            if child.text != None :
                reqAttributeData = child.text
                # This part is used if we want to have the final answer in separate files which didn't look so appealing.
                # if attribute == "data":
                #     reqAttributeDataList = nltk.sent_tokenize(reqAttributeData)
                #     reqAttributeData = ""
                #     for sent in reqAttributeDataList:
                #         reqAttributeData =  reqAttributeData + sent + "\n"
    return reqAttributeData

tree = ET.parse(filePath + "/" + fileName + ".xml")
root = tree.getroot()
documentRoot = root[0]

db_funcs.delete_data("topic_map")
db_funcs.delete_data("topic_data")

# Adds root's parent as "root"
db_funcs.add_topic("root",findSecAttribute(documentRoot,"name"))
db_funcs.add_data(findSecAttribute(documentRoot,"name"),findSecAttribute(documentRoot,"data"))

def myDfs(root):
    rootName = findSecAttribute(root,"name")
    for child in root :
        if(child.tag == "section") :
            myDfs(child)
            sectionName  = findSecAttribute(child,"name")
            sectionData  = findSecAttribute(child,"data")

            # changes the encoding to ascii
            sectionName = sectionName.encode('ascii', 'ignore').decode('ascii')
            sectionData = sectionData.encode('ascii', 'ignore').decode('ascii')
            rootName = rootName.encode('ascii', 'ignore').decode('ascii')

            # strips leading and trailing spaces
            sectionName = sectionName.strip()
            sectionData = sectionData.strip()
            rootName = rootName.strip()

            db_funcs.add_topic(rootName, sectionName)
            db_funcs.add_data(sectionName, sectionData)
myDfs(documentRoot)