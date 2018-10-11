# -*- coding: utf-8 -*-
"""
Created on Mon May 21 13:56:54 2018

@author: mohsheik
"""

import requests
from requests.auth import HTTPDigestAuth
from mlutils import generateSearchPayload, generatePUTPayload, syntacticMatchingScore, getMLResults, getAllFromNeo4j 
import hashlib
import json
from operator import itemgetter

session = requests.session()
session.auth = HTTPDigestAuth("admin", "admin")
headers = {'Content-Type': "application/json",'Cache-Control': "no-cache",'Postman-Token': "cb314800-421b-39c8-56e9-1c89f5787fe4" }
#baseUri = "http://localhost:8002/manage/v2/databases"
#response = session.get("http://localhost:8002/manage/v2/databases?format=json")

   
def getEntity(query):
    url = "http://127.0.0.1:8020/v1/search?format=json"
    #query = "hello one"
    payload = generateSearchPayload(query)    
    uresponse = session.request("POST", url, data=payload, headers=headers)

    print(uresponse.status_code)
    #print("RESPONSE: ",uresponse.json())

    result = uresponse.json()
    mlResult = getMLResults(result)
    #print("ML Result", mlResult)

    scoredResults =[]
    
    for result in mlResult:
        name = result["name"]
        score=syntacticMatchingScore(name.lower(),query.lower())
        scoredDict = {}
        #if float(score) > 0.5:
        scoredDict["name"]=result["name"]
        scoredDict["score"]=score
        scoredDict["entity_class"]=result["entity_class"]
        scoredDict["id"]=result["id"]
        scoredResults.append(scoredDict)
        
    scoredResultsSorted = sorted(scoredResults, key=itemgetter('score'),reverse = True)
    json_result_entity = json.dumps(scoredResultsSorted)
    print ("Scored Results: ", json_result_entity)
    return json_result_entity



def putEntity(entityName, uri, fileName):
    json_payload = generatePUTPayload(entityName,uri)
    #print ("JSON: ",json_payload)
    uploadurl = "http://127.0.0.1:8020/v1/documents?uri="+ fileName+ ".json"
    #print ("UPLOAD URL:" + uploadurl)
    uresponse = session.request("PUT", uploadurl, data=json_payload, headers=headers)
    print(uresponse.status_code)


#entityName = "Premier League"
#uri = "IPL.com"
#fileName = "ipl1"
#print (putEntity(entityName, uri, fileName))

#resolveEntity = "Energy Supply"
#resolveEntity = "morgan stanley"
#resolveEntity = "totally different"
resolveEntity = "Chevron Enregy"
#resolveEntity = "Shell Gas"
#resolveEntity = "comstock resources"
getEntity(resolveEntity)

def importNeo4JtoML():
    allTerms = getAllFromNeo4j("http://localhost", "7673", "neo4j", "neo4j1")
    #allTerms = getAllFromNeo4j("http://10.207.16.63", "7673", "neo4j", "neo4j1")

    for term in allTerms:
        pvalue = term['Phrases']
        puri = term['URI']
        plabel = term['Label']
        unique_id_str = pvalue + puri
        unique_id = hashlib.md5(unique_id_str.encode()).hexdigest()
        filename = plabel + "_"+ unique_id
        print(filename)
        putEntity(pvalue, puri, filename)
    
#importNeo4JtoML()   ]')






