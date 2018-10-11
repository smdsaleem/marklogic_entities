# -*- coding: utf-8 -*-
"""
Created on Tue May 29 09:46:56 2018

@author: mohsheik
"""
from nltk.tokenize import word_tokenize
from neo4jrestclient.client import GraphDatabase
import json
import numpy as np
from math import sqrt
from NGrams import Ngrams, CharNgrams
from metaphone import get_company_dm
from operator import itemgetter


def generateSearchPayload(queryString):
    wordtokens = word_tokenize(queryString)
    startQuery = "{  \"$query\" : { \"$or\": [ "
    endQuery =  "]  }}"
    singleQuery = "{ \"phrases\": {\"$word\": \"word_to_replace\" }, \"$case-sensitive\": false, \"$exact\":false, \"$stemmed\":true}"
    alltokens = []
    metaphones = get_company_dm(queryString)
    metaphonestokens =  word_tokenize(metaphones)
    alltokens = wordtokens + metaphonestokens
    #print ("Word Tokens:", wordtokens)
    #print ("All tokens:",alltokens )
    for w in alltokens:
    #for w in wordtokens:
        copyQuery = singleQuery.replace("word_to_replace", w)
        if alltokens.index(w) > 0:
            copyQuery = ", " + copyQuery
        startQuery = startQuery + copyQuery
    finalQuery = startQuery + endQuery
    return finalQuery

#print (generateSearchPayload("Mahammad Salim Sheikh"))
            
def generatePUTPayload(entityName, uri):
    uploadDoc ={}
    uploadDoc["filename"] = uri
    myphrases = word_tokenize(entityName)
    mymetaphones = []
    fullString = ''
    for p in myphrases:
        fullString = fullString + " " + get_company_dm(p)
 
    mymetaphones.append(entityName.lower() + " (" + fullString.strip() + ")")
    #uploadDoc["phrases"] = mymetaphones    
    uploadDoc["phrases"] = entityName.lower()
    json_string = json.dumps(uploadDoc)
    return json_string

#print (generatePUTPayload("Mohammad Saleem Sheik","1"))

def getAllFromNeo4j(hostname, port, uname, pwd):
    url = hostname+":"+port
    db = GraphDatabase(url, username=uname, password=pwd)
    query = 'MATCH (n) return n,labels(n)'
    results = db.query(q=query)
    allTerms = []
    for r in results:  
        matchedTerm = {}
        try:
            #print r
            label = str(r[1][0])
            node_name = str(r[0]['data']['name'])
            uri = str(r[0]['data']['uri'])
            matchedTerm["Label"]=label
            myphrases = node_name
            matchedTerm["Phrases"]=myphrases
            matchedTerm["URI"]=uri
            #print("### Label:", label)
            #print("### Entity: ",node_name)
            #print("### URI: ",uri)
        except IndexError:
            print ("$$$$$ IndexError for %s")
        if label != 'Document':
            allTerms.append(matchedTerm)
    #print("----  All Terms: ",allTerms)
    return allTerms

#print (getAllFromNeo4j("http://localhost", "7673", "neo4j", "neo4j1"))

def getMLResults(result):
    entityList = []
    entityDictList = []
    
    #print(result['total'])
    for hit in result['results']:
        for matches in hit["matches"]:
            score = hit["score"]
            uri = hit["uri"]
            entity_class = str(uri.split('_', 1)[0])
            idn = ''
            try:
                idn = str(uri.split('_', 1)[1]).split('.', 1)[0]
            except IndexError:
                idn = ''

            #print ("----- matches:: ", matches)
            entity = ''
            for matchtext in matches["match-text"]:
                #print ("MATCHTEXT:::: ", str(matchtext))
                if (not (str(matchtext) and str(matchtext).strip())):
                    #print("EMPTY !!!!")
                    entity = entity + ' '
                elif type(matchtext) is dict:
                    if not (matchtext["highlight"].isupper()):
                        entity = entity + matchtext["highlight"]
                        #print("YES!!!! :", matchtext["highlight"] )
    
                else :
                    if not (matchtext.isupper()):
                       #print("NOOOO !!! :",matchtext)
                       indx=len(matchtext)
                       try:
                           indxStart = matchtext.index("(")  
                           #print ("Start Index:",indxStart )
                           if(indxStart)!=-1:
                               indx = indxStart
                       except ValueError:
                           donothing = 0

                           
                       try:
                           indxEnd = matchtext.index(")")
                           #print ("End Index:",indxEnd )
                       except ValueError:
                           donothing = 0

 
                       entity = entity +  matchtext[0:indx]
                       
            finalentity = entity.replace("("," ")
            finalentity = finalentity.replace(")"," ")
            finalentity = finalentity.strip()
            #print ("Final !!!! : " + finalentity)
            #entityList.append(entity)
            if ((str(finalentity) and str(finalentity).strip())):
                entityDict = {}
                entityDict["name"] = finalentity
                entityDict["score"] = score
                entityDict["entity_class"]= entity_class
                entityDict["id"] = idn
                entityList.append(entityDict)
                
 
    entityDictList = sorted(entityList, key=itemgetter('score'),reverse = True)
    print("Sorted Entities:", entityDictList)
    return entityDictList


def getML1Results(result):
    entityList = []
    entityDictAll = {}
    entityDict = {}
    #print(result['total'])
    for hit in result['results']:
        for matches in hit["matches"]:
            score = hit["score"]
            uri = hit["uri"]
            entity_class = str(uri.split('_', 1)[0])
            idn = ''
            try:
                idn = str(uri.split('_', 1)[1]).split('.', 1)[0]
            except IndexError:
                idn = ''
            print("uri", uri)
            print("entity_class", entity_class)
            print("idn", idn)
            #print("idnum",idnum)
            #print ("----- matches:: ", matches)
            entity = ''
            for matchtext in matches["match-text"]:
                #print ("MATCHTEXT:::: ", str(matchtext))
                if (not (str(matchtext) and str(matchtext).strip())):
                    #print("EMPTY !!!!")
                    entity = entity + ' '
                elif type(matchtext) is dict:
                    if not (matchtext["highlight"].isupper()):
                        entity = entity + matchtext["highlight"]
                        #print("YES!!!! :", matchtext["highlight"] )
    
                else :
                    if not (matchtext.isupper()):
                       #print("NOOOO !!! :",matchtext)
                       indx=len(matchtext)
                       try:
                           indxStart = matchtext.index("(")  
                           #print ("Start Index:",indxStart )
                           if(indxStart)!=-1:
                               indx = indxStart
                       except ValueError:
                           donothing = 0

                           
                       try:
                           indxEnd = matchtext.index(")")
                           #print ("End Index:",indxEnd )
                       except ValueError:
                           donothing = 0

                           #print("IGNORE")   
                       #print("NOOOO 2 !!! :", matchtext[0:indx])   
                       entity = entity +  matchtext[0:indx]
            finalentity = entity.replace("("," ")
            finalentity = finalentity.replace(")"," ")
            finalentity = finalentity.strip()
            #print ("Final !!!! : " + finalentity)
            #entityList.append(entity)
            if ((str(finalentity) and str(finalentity).strip())):
                #entityDict["name"] = finalentity
                #entityDict["score"] = score
                #entityDict["entity_class"]= entity_class
                #entityDict["id"] = idn
                #entityList.append(entityDict)
                entityDict[finalentity]=score

                
    #print("Entity List: ", entityList)
    print("Entity Result:", entityList)
    
    for key in sorted(entityDict.iterkeys(), reverse=True )[:100]:
        #print ("%s: %s" % (key, entityDict[key]))
        entityList.append(str(key))
        #entityDictSorted[key] = entityDict[key]
    
    #print("Sorted Entities:", entityDictSorted)
    return entityList
#getAllFromNeo4j("http://localhost","7673", "neo4j", "neo4j1")  
    
def levenshteinDistance(str1, str2):
    m = len(str1)
    n = len(str2)
    lensum = float(m + n)
    d = []           
    for i in range(m+1):
        d.append([i])        
    del d[0][0]    
    for j in range(n+1):
        d[0].append(j)       
    for j in range(1,n+1):
        for i in range(1,m+1):
            if str1[i-1] == str2[j-1]:
                d[i].insert(j,d[i-1][j-1])           
            else:
                minimum = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+2)         
                d[i].insert(j, minimum)
    ldist = d[-1][-1]
    ratio = (lensum - ldist)/lensum
    return ratio

#print ("levenshteinDistance: ", levenshteinDistance("Morgan Stanley", "Murgan Stanley"))


def syntacticMatchingScore(str1, str2):
    ngram_score=Ngrams(str1) * Ngrams(str2)
    lev_score=0
    char_gram_score=0
    lev_score=levenshteinDistance(str1,str2)
    char_gram_score=CharNgrams(str1)*CharNgrams(str2)
    #softidf_score=getIdfScore(str1, str2, idfDict, avg_score)
    matchingScore= max(ngram_score,max(char_gram_score,lev_score))    
    matchingScore=format(matchingScore, '.5f')
    return matchingScore

#print ("syntacticMatchingScore: ", syntacticMatchingScore("Morgan Stanley", "Murgan Stanley"))
    
def cosine_sim(u,v):
    return np.dot(u,v) / (sqrt(np.dot(u,u)) * sqrt(np.dot(v,v)))

#phrase1 = np.array(list("morgan mtanley"),dtype=int)
#phrase2 = np.array(list("murgan mtanley"),dtype=int)
#print("Test Cosine:", cosine_sim(phrase1, phrase2) )