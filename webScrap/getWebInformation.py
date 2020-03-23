import numpy as np
#import pandas as pd
import requests as rq
import re
from bs4 import BeautifulSoup
try: 
	from googlesearch import search 
except ImportError: 
	print("No module named 'google' found") 


def webForWiki(plantName):
    url = "https://www.easyatm.com.tw/wiki/" + plantName # 百科知識 
    needSite = "easyatm.com.tw"
    urlList = getNeedURL(plantName, needSite)
    for theurl in urlList:
        if theurl.find(needSite) > -1:
            url = theurl
            break
    try:
        response = rq.get(url) # 用 requests 的 get 方法把網頁抓下來
        html_doc = response.text # text 屬性就是 html 檔案
        #soup = BeautifulSoup(response.text, "lxml") # 指定 lxml 作為解析器
        soup = BeautifulSoup(html_doc, "lxml") # 指定 lxml 作為解析器
        #posts = soup.find("div")
    except:
        return None
    #posts = soup.find("div")
    parts = soup.find_all("div", attrs = {"id":"content"})
    part_word = []
    for part in parts:
        part_word.extend(part.find_all("p"))
    return part_word 


def webForWikiAgain(plantName, keywords = []):
    url = "https://www.easyatm.com.tw/wiki/" + plantName # 百科知識 
    needSite = "easyatm.com.tw"
    urlList = getNeedURL(plantName, needSite)
    for theurl in urlList:
        if theurl.find(needSite) > -1:
            url = theurl
            break
    try:
        response = rq.get(url) # 用 requests 的 get 方法把網頁抓下來
        html_doc = response.text # text 屬性就是 html 檔案
        #soup = BeautifulSoup(response.text, "lxml") # 指定 lxml 作為解析器
        soup = BeautifulSoup(html_doc, "lxml") # 指定 lxml 作為解析器
        #posts = soup.find("div")
    except:
        return None

    part_word = soup.find_all("li")
    '''
    parts = soup.find_all("div", attrs = {"id":"content"})
    part_word = []
    for part in parts:
        part_word.extend(part.find_all("p"))

    parts = soup.find_all("div")
    part_word = []
    for part in parts:
        part_word.extend(part.find_all("p"))

    '''
    return_part_word = []
    for part in part_word:
        part = str(part)
        part = "".join(part.split())
        #print(part)
        for keyword in keywords:
            checkText = part.find(keyword)
            if not checkText == -1:
                return_part_word.append(part)
                break
    return return_part_word 


def webForPH():
    url = "https://www.gardenexpress.com.au/soil-ph-guide/" # 澳洲ph值網站 
    try:
        response = rq.get(url) # 用 requests 的 get 方法把網頁抓下來
        html_doc = response.text # text 屬性就是 html 檔案
        soup = BeautifulSoup(html_doc, "lxml") # 指定 lxml 作為解析器
    except:
        return None
    #posts = soup.find("div")
    parts = soup.find_all("section", attrs = {"id":"main"})
    part_word = []
    returnList = []
    #thefile = open("ph.csv","a")

    for part in parts:
        part_word.extend(part.find_all("td"))
    for part in part_word:
        part = str(part)
        part = "".join(part.split())
        part = delWord(part)
        returnList.append(part)
    returnList[-2] = "Zinnia"

    '''
    for index, i in enumerate(returnList):
        if index / 2 == 0:
            thefile.write(i + ",")
        else:
            thefile.write(i + "\n")
    '''
    #soup.select('div.g > h3.r > a[href^="/url"]')
    return url, returnList


def webForKplant(plantName):
    url = "http://kplant.biodiv.tw/" + plantName + "/" + plantName + ".htm" # 台灣一個植物特微說明網站 
    needSite = "kplant.biodiv.tw"
    urlList = getNeedURL(plantName, needSite)
    for theurl in urlList:
        if theurl.find(needSite) > -1:
            url = theurl
            break

    try:
        response = rq.get(url) # 用 requests 的 get 方法把網頁抓下來
        response.encoding = response.apparent_encoding
        html_doc = response.text # text 屬性就是 html 檔案
        soup = BeautifulSoup(html_doc, "lxml") # 指定 lxml 作為解析器
    except:
        return None
    parts = soup.find_all("tr")
    part_word = []
    #主要是抓植物的別名與英文名，所以回傳要的值即可
    titleString = "中文名稱"
    titleStrings = ["中文名稱", "英文名稱", "學名", "科名", "別名"]
    untilString = "原產地"
    returnList = []
    for part in parts:
        part_word.extend(part.find_all("span"))
    check = False
    for part in part_word:
        part = str(part)
        part = "".join(part.split())
        part = part.replace("\n", "")
        if not part.find(titleString) == -1:
            check = True
        if not part.find(untilString) == -1:
            break
        if check:
            part = delWord(part)
            returnList.append(part)
    return returnList


def delWord(word, startWord = "<", endWord = ">"):
    startIndex = -1
    endIndex = -1
    
    for i in range(len(word)):
        if word[i] == startWord:
            startIndex = i
            continue
        if word[i] == endWord and startIndex > -1:
            endIndex = i
            processWord = ""
            processWord = word[:startIndex] + word[endIndex + 1:]
            word = processWord
            break
    if startIndex == -1 or endIndex == -1:
        return word
    else:
        return delWord(word, startWord, endWord)


def getInformationFromWeb(url, keywords = []):
    try:
        response = rq.get(url) # 用 requests 的 get 方法把網頁抓下來
        response.encoding = response.apparent_encoding
        html_doc = response.text # text 屬性就是 html 檔案
        #soup = BeautifulSoup(response.text, "lxml") # 指定 lxml 作為解析器
        soup = BeautifulSoup(html_doc, "lxml") # 指定 lxml 作為解析器
        #posts = soup.find("div")
    except:
        return None 

    parts = soup.find_all("div")
    part_word = []
    for part in parts:
        part_word.extend(part.find_all("p"))

    return_part_word = []
    for part in part_word:
        part = str(part)
        part = "".join(part.split())
        if isinstance(keywords, list):
            for keyword in keywords:
                checkText = part.find(keyword)
                if not checkText == -1:
                    return_part_word.append(part)
                    break
        else:
            checkText = part.find(keywords)
            if not checkText == -1:
                return_part_word.append(part)
    return return_part_word


def getNeedURL(plantName, searchParam = ""):
    if searchParam:
        query = plantName + " " + searchParam
    else:
        query = plantName
    print(query)
    #searchList = search(query, tld="co.in", lang="zh-TW", stop = 10, pause=2) 
    searchList = search(query, lang="zh-TW", stop = 5, pause=2) 
    return searchList


def getNeedEngURL(plantName, searchParam = ""):
    if searchParam == "":
        query = plantName
    else:
        query = plantName + " " + searchParam
    print(query)
    searchList = search(query, stop = 5, pause=2) 
    return searchList


if __name__ == "__main__":
    #plantName = "薰衣草"
    plantDictionary = {}
    plantDictionary["中文名稱"] = "薰衣草"
    #x = getNeedURL("向日葵", " site:http://kplant.biodiv.tw/")
    #webForPH()
    #webForWiki("仙人掌")
    #webForWikiAgain("仙人掌")

