import numpy as np
import json
import pandas as pd
import requests as rq
import re
import myString
import getWebInformation as myWeb
import plantDB as myDB
from bs4 import BeautifulSoup


tempuratureTitle = myString.getTempuratureName()
moistureTitle = myString.getMoistureName()
phTitle = myString.getPhName()
sunlightTitle =  myString.getSunlightName()

ChineseName = myString.getPlantCName()
EnglishName = myString.getPlantEName()
ScientificName = myString.getPlantSName()
Order = myString.getPlantOrder()
OtherName = myString.getPlantOName()

def formatOutput(needFormatWord, removeWords = [], startWord = "", endWord = ""):
    for removeWord in removeWords: #清空文字以統一
        needFormatWord = needFormatWord.replace(removeWord, "")
    needFormatWord = startWord + needFormatWord + endWord
    return needFormatWord


def findKeywords(keywordType, answerList):
    answer = "" 
    if keywordType ==  "溫度":
        #格式
        formatString = [r'\d{1,2}-\d{1,2}°C', r'\d{1,2}-\d{1,2}℃', r'攝氏\d{1,2}-\d{1,2}', r'\d{1,2}°C-\d{1,2}°C', r'\d{1,2}℃-\d{1,2}℃'] #溫度的格式
        formatRemoveWord = ["攝氏", "℃", "°C"]
        for showList in answerList:
            for formatWord in formatString:
                #找出特定的格式(XX-XX)
                keywords = re.compile(formatWord)
                findanswer = keywords.findall(showList)
                if findanswer:
                    answer = findanswer[0]
                    #統一格式
                    answer = formatOutput(answer, removeWords=formatRemoveWord, endWord="℃")
            if answer:
                break
    else:
        print("Error")
    if not answer:
        print("Not Found！")
    return answer


def findPhWord(webText, keywordList):
    for i, text in enumerate(webText):
        for keyword in keywordList:
            result = text.find(keyword)
            if result > -1:
                return webText[i+1]
    return ""


def wordStartToEnd(locate = 0, textLen = 0, period = 20):
    textStart = locate - 20
    if textStart < 0: 
        textStart = 0
    textEnd = locate + 20
    if textEnd > textLen:
        textEnd = textLen
    return textStart, textEnd


def findWord(text_list = [], find_word = [], except_word = [], period = 20, priority_word = []):
    answerList = []
    for text in text_list: # 找剛截下來的字串陣列
        text = str(text)
        text = text.replace("~", "-") # 統一區間的文字
        text = text.replace("～", "-")
        for word in find_word:   # 關鍵字陣列
            while True:
                checkAnswer = text.find(word)
                if not(checkAnswer == -1):  # 不是-1表示有找到
                    textStart, textEnd = wordStartToEnd(locate = checkAnswer, textLen = len(text), period = period)
                    # 選取要截取的段落
                    newText = text[textStart:textEnd]
                    for exceptWord in except_word: # 表示有不想截取的內容
                        checkAnswerAgain = newText.find(exceptWord)
                        if not(checkAnswerAgain == -1): #有找到不想截取的內容
                            newText = ""
                            break
                    #print(text[textStart:textEnd])
                    if not newText:
                        answerList.append(newText)
                        p_min = period / 2 - 4
                        p_max = period / 2 + 4
                        except_word.append(newText[p_min : p_max]) # 除去重覆的字串
                    text = text[textEnd:]
                else:
                    break

    for index, answer in enumerate(answerList):
        check = False
        for p in priority_word:
            if answer.find(p) > -1:
                temp = answerList[0]
                answerList[0] = answer
                answerList[index] = temp
                check = True
                break
        if check:
            break
    return answerList


def callFindWord(text_list = [], find_word = [], except_word = [], period = 20, priority_word = []):
    answerList = findWord(text_list, find_word, except_word, priority_word = priority_word)
    answer = findKeywords(keywordType = find_word[0], answerList = answerList)
    return answer 


def loopForCallFindWord(plantName, search_Param, find_word = [], except_word = [], period = 20, priority_word = []):
    part_word = []
    getInformation = ""
    #拿到google搜尋結果
    urlList = myWeb.getNeedURL(plantName, search_Param)
    for theURL in urlList:
        #檢查網站內是否有要查找的關鍵字
        part_word = myWeb.getInformationFromWeb(theURL, find_word)
        if part_word:
            returnResult = callFindWord(text_list = part_word, find_word = find_word, except_word = except_word, period = period, priority_word = priority_word)
            if returnResult:
                #表示有找到結果
                getInformation = returnResult
                break
    return getInformation 


def getPlantOtherName(plantName):
    titleStrings = myString.getTitleStrings()
    titleDictionary = [ChineseName, EnglishName, ScientificName, Order, OtherName]
    myDictionary = {ChineseName : [],
                    EnglishName : [],
                    ScientificName : [],
                    Order : [],
                    OtherName : []}
    myDictionary = myDB.getPlantName(plantName)
    
    #表示資料庫有資料
    if len(myDictionary[OtherName]) > 0:
        return myDictionary

    returnList = []
    index = 0
    delWordList = ["：", "、", "，", "‧", "\n"]

    webTextList = myWeb.webForKplant(plantName)
    theUrl = ""
    if webTextList is None:
        theUrl = myWeb.getNeedURL(plantName, "別名")
        webTextList = myWeb.getInformationFromWeb(plantName, ["別名"])

    for scraping in webTextList:
        leftBracket = ["『","（"]
        rightBracket = ["』","）"]
        #統一括號的格式
        for k in leftBracket:
            scraping = scraping.replace(k,"(")
        for k in rightBracket:
            scraping = scraping.replace(k,")")

        for i in range(len(delWordList)):
            scraping = scraping.replace(delWordList[i], ".")
        scraping = scraping.replace(" ", "")
        scraping = scraping.replace("\r", " ")
        scraping = "".join(scraping.split())
        splitStrings = scraping.split(".")
        for splitString in splitStrings:
            if splitString == "":
                continue
            if isinstance(titleStrings[index + 1],list):
                oldIndex = index
                for theTitle in titleStrings[index + 1]:
                    if splitString == theTitle:
                        index = index + 1
                if oldIndex < index:
                    continue
            else:
                if splitString == titleStrings[index + 1]:
                    index = index + 1
                    continue
            myDictionary[titleDictionary[index]].append(splitString)
    myDictionary[ChineseName] = plantName
    
    formatString = re.compile(r'\w+')
    updateList = []
    for item in myDictionary[Order]:
        text = formatString.findall(item)
        updateList.extend(text)
    myDictionary[Order] = updateList
    #表示科名那一欄有圖片
    if len(myDictionary[Order]) > 4:
        myDictionary[Order] = myDictionary[Order][0:4]

    updateList = []
    #用以檢查是否為()內的內容
    check = True
    #去除()與其他
    for i, item in enumerate(myDictionary[ScientificName]):
        if not check:
            check = True
            continue

        if item.find("(") == -1:
            item = item.replace(")", "")
            updateList.append(item)

        if item.encode("UTF-8").isalpha():
            updateList.append(item)
        '''
        else:
            updateList.append(item[:-1])
            check = False
            continue
        '''

    myDictionary[ScientificName] = updateList

    updateList = []
    #用以檢查是否為()內的內容
    check = True
    #去除別名的()
    for i, item in enumerate(myDictionary[OtherName]):
        if not check:
            check = True
            continue

        if item.find("(") == -1:
            item = item.replace(")", "")
            updateList.append(item)
        else:
            if item.find("(") >= len(item) -1:
                updateList.append(item[:-1])
                check = False
            else:
                updateList.append(item[0:item.find("(")])
            continue

    myDictionary[OtherName] = updateList

    #表示科名那一欄有圖片
    if len(myDictionary[Order]) > 4:
        myDictionary[Order] = myDictionary[Order][0:4]

    #print(myDictionary)
    #記錄
    if len(myDictionary[OtherName]) > 1:
        myDB.setPlantName(myDictionary)
    return myDictionary


def findMoistureWord(webText, keywordList):
    for i, text in enumerate(webText):
        for keyword in keywordList:
            result = text.find(keyword)
            if result > -1:
                return webText[i+1]
    return ""


def findSunlightWord(text_list, find_word, countList):
    # test
    for text in text_list: # 找剛截下來的字串陣列
        text = str(text)
        for index, word in enumerate(find_word):   # 關鍵字陣列
            countList[index] += 1

    '''
    for i, text in enumerate(webText):
        for keyword in keywordList:
            result = text.find(keyword)
            if result > -1:
                return webText[i+1]
    '''
    return countList

def findSunlight(plantName, search_Param, find_word = [], except_word = [], period = 60):
    countList = []
    for i in range(len(find_word)):
        countList.append(0)
    part_word = []
    getInformation = ""
    #拿到google搜尋結果
    #urlList = myWeb.getNeedURL(plantName, search_Param)
    for thename in plantName:
        urlList = myWeb.getNeedEngURL(thename, search_Param)
    
        for theURL in urlList:
            #檢查網站內是否有要查找的關鍵字
            part_word = myWeb.getInformationFromWeb(theURL, find_word)
            if not part_word is None:
                #returnResult = findWord(text_list = part_word, find_word = find_word, except_word = except_word, period = period)
                text_list = findWord(text_list = part_word, find_word = find_word, period = 80)
                countList = findSunlightWord(text_list = text_list, find_word = find_word, countList = countList)
                #countList[index] += 1
    maxIndex = countList.index(max(countList))
    return find_word[maxIndex]


def getTempuratureInformation(plantDictionary):
    returnList = {tempuratureTitle : "" }
    plantName = plantDictionary[ChineseName]
    #從資料庫找溫度
    returnList[tempuratureTitle] = myDB.getTempurature(plantDictionary[ChineseName])
    tempuratureText = ["溫度", "適溫", "°C", "℃", "攝氏"] #統一第一個字為標題
    tempuratureExceptText = ["病"]
    tempuratureTextofPriority = ["生長適溫","合適溫度", "適宜溫度", "合適的溫度", "適宜的溫度"]

    #從植物百科截取需要的溫度資訊
    if not returnList[tempuratureTitle]:
        part_word = myWeb.webForWiki(plantName)
        returnResult = callFindWord(text_list = part_word, find_word = tempuratureText, except_word = tempuratureExceptText, period = 20, priority_word = tempuratureTextofPriority)
        if not returnResult == "":
            returnList[tempuratureTitle] = returnResult
            myDB.setTempurature(plantDictionary[ChineseName], returnResult)
    
    #再一次從植物百科截取需要的溫度資訊
    if not returnList[tempuratureTitle]:
        part_word = myWeb.webForWikiAgain(plantName, tempuratureText)
        returnResult = callFindWord(text_list = part_word, find_word = tempuratureText, except_word = tempuratureExceptText, period = 20, priority_word = tempuratureTextofPriority)
        if returnResult == "":
            print("esayatm Not Found")
        else:
            returnList[tempuratureTitle] = returnResult
            myDB.setTempurature(plantDictionary[ChineseName], returnResult)

    #測試！從外部網站截取需要的溫度資訊
    if not returnList[tempuratureTitle]:
        temp = loopForCallFindWord(plantName = plantDictionary[ChineseName], search_Param = "溫度", find_word = tempuratureText, except_word = tempuratureExceptText, period = 40, priority_word = tempuratureTextofPriority)
        '''
        if temp:
            for item in plantDictionary[OtherName]:
                # 還在測試階段
                temp = loopForCallFindWord(plantName = item, search_Param = "溫度", find_word = tempuratureText, except_word = tempuratureExceptText, period = 40)
                if temp:
                    break
        '''
        if temp:
            returnList[tempuratureTitle] = temp 
            myDB.setTempurature(plantDictionary[ChineseName], temp)
        else:
            print("Google Search of tempurature not found")

    '''
    #用別名找資料庫資料
    if not returnList[tempuratureTitle]:
        for name in plantDictionary[OtherName]:
            tempurature = myDB.getTempurature(name)
            if not tempurature == "":
                returnList[tempuratureTitle] = tempurature
                break
        if not returnList[tempuratureTitle]:
            print("Tempurature Not Found")
    '''

    return returnList[tempuratureTitle]


def getPhInformation(plantDictionary):
    returnList = {phTitle : ""}
    #ph值
    returnList[phTitle] = myDB.getPh(plantDictionary[EnglishName])
    if returnList[phTitle] == "":
        for name in plantDictionary[Order]:
            ph = myDB.getPh(name)
            if not ph == "":
                returnList[phTitle] = ph
                break
    '''
    if returnList[phTitle] == "":
        webTextList = myWeb.webForPH()
        returnResult = findPhWord(webTextList, plantDictionary[Order])
        if returnResult == "":
            returnResult = findPhWord(webTextList, plantDictionary[EnglishName])
            if returnResult == "":
                print("Error")
            else:
                returnList[phTitle] = returnResult
        else:
            returnList[phTitle] = returnResult
            myDB.setPh(plantDictionary[EnglishName], returnResult)
    '''
    return returnList[phTitle]


def getMoistureInformation(plantDictionary):
    returnList = {moistureTitle : ""}
    #Moisture
    returnList[moistureTitle] = myDB.getMoisture(plantDictionary[EnglishName])
    if returnList[moistureTitle] == "":
        for name in plantDictionary[Order]:
            moisture = myDB.getMoisture(name)
            if not moisture == "":
                returnList[moistureTitle] = moisture
                break
    '''
    if returnList[moistureTitle] == "":
        #---------------------------------------------------------
        webTextList = myWeb.getInformationFromWeb()
        returnResult = findMoistureWord(webTextList, plantDictionary[EnglishName])
        if returnResult == "":
            returnResult = findMoistureWord(webTextList, plantDictionary[Order])
            if returnResult == "":
                print("Error")
            else:
                returnList[moistureTitle] = returnResult
        else:
            returnList[moistureTitle] = returnResult
            myDB.setMoisture(plantDictionary[EnglishName], returnResult)
    '''
    return returnList[moistureTitle]


def getSunlightInformation(plantDictionary):
    returnList = {sunlightTitle : ""}
    #Sunlight
    returnList[sunlightTitle] = myDB.getSunlight(plantDictionary[EnglishName])
    if returnList[sunlightTitle] == "":
        for name in plantDictionary[Order]:
            sunlight = myDB.getSunlight(name)
            if not sunlight == "":
                returnList[sunlightTitle] = sunlight
                break

    searchTextForChinese = ["全日照", "半日照", "半陰", "陰蔽"]
    searchTextForEnglish = ["full sun", "partial shade", "full shade"]

    if returnList[sunlightTitle] == "":
        #---------------------------------------------------------
        result = findSunlight(plantDictionary[EnglishName], "sun requirements", searchTextForEnglish, period = 150)
        if not result:
            returnList[sunlightTitle] = searchTextForChinese[searchTextForEnglish.index(result)]
            myDB.setSunlight(plantDictionary[EnglishName], returnList[sunlightTitle])
            return returnList[sunlightTitle]

        result = findSunlight(plantDictionary[Order], "sun requirements", searchTextForEnglish, period = 150)
        if not result:
            returnList[sunlightTitle] = searchTextForChinese[searchTextForEnglish.index(result)]
            myDB.setSunlight(plantDictionary[EnglishName], returnList[sunlightTitle])
            return returnList[sunlightTitle]

        result = findSunlight(plantDictionary[ChineseName], "sun requirements", searchTextForChinese, period = 60)
        if not result:
            returnList[sunlightTitle] = result
            myDB.setSunlight(plantDictionary[EnglishName], returnList[sunlightTitle])
            return returnList[sunlightTitle]


        result = findSunlight(plantDictionary[OtherName], "sun requirements", searchTextForChinese, period = 60)
        if not result:
            returnList[sunlightTitle] = result
            myDB.setSunlight(plantDictionary[EnglishName], returnList[sunlightTitle])
            return returnList[sunlightTitle]
    return returnList[sunlightTitle]


def getInformation(plantName):
    returnList = {tempuratureTitle:"", phTitle:"", moistureTitle: "" , sunlightTitle: ""} 
    #抓其他別名
    plantDictionary = getPlantOtherName(plantName)

    #Tempurature
    returnList[tempuratureTitle] = getTempuratureInformation(plantDictionary)

    #ph
    returnList[phTitle] = getPhInformation(plantDictionary) 

    #Moisture
    returnList[moistureTitle] = getMoistureInformation(plantDictionary)

    #sunlight
    returnList[sunlightTitle] = getSunlightInformation(plantDictionary)
    return returnList


def webScrap(plantName):
    print("call function : webScrap , plantName = ", plantName)
    #主程式
    getNeedInfo = getInformation(plantName)
    returnJson = json.dumps(getNeedInfo)
    return returnJson
    #return getNeedInfo 


if __name__ == "__main__":
    plantName = input("查詢的植物：")
    if plantName == "":
        plantName = "含羞草"
    print("搜尋：", plantName)
    info = webScrap(plantName = plantName)
    print(info)

