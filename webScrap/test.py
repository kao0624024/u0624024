import getWebInformation as  myWeb
import webScraping as ms 
try: 
	from googlesearch import search 
except ImportError: 
	print("No module named 'google' found") 

# to search 
plantDictionary = ms.getPlantOtherName("百日草")
#query = "百日草"
#search(query, tld = "com", lang = "en", num = 10, start = 0, stop = None, pause = 2.0)

#測試！從外部網站截取需要的溫度資訊
searchTextForChinese = ["全日照", "半日照", "半陰", "陰蔽"]

searchTextForEnglish = ["full sun", "partial shade", "full shade"]


def findWord(text_list = [], find_word = [], except_word = [], period = 20, keywordType = ""):
    answerList = []
    answer = ""
    for text in text_list: # 找剛截下來的字串陣列
        text = str(text)
        text = text.replace("~", "-") # 統一區間的文字
        text = text.replace("～", "-")
        for word in find_word:   # 關鍵字陣列
            checkAnswer = text.find(word)
            if not(checkAnswer == -1):  # 不是-1表示有找到
                textStart, textEnd = ms.wordStartToEnd(locate = checkAnswer, textLen = len(text), period = period)
                # 選取要截取的段落
                newText = text[textStart:textEnd]
                for exceptWord in except_word: # 表示有不想截取的內容
                    checkAnswerAgain = newText.find(exceptWord)
                    if not(checkAnswerAgain == -1): #有找到不想截取的內容
                        newText = ""
                        break
                #print(text[textStart:textEnd])
                if not(newText == "" ):
                    answerList.append(newText)
                    except_word.append(newText[7:13]) # 除去重覆的字串
    #answer = findKeywords(keywordType = keywordType, answerList = answerList)
    #return answer
    return answerList


def loopForCallFindWord(plantName, search_Param, find_word = [], except_word = [], period = 20):
    countDictionary = {searchTextForEnglish[0]:0, searchTextForEnglish[1] :0, searchTextForEnglish[2] : 0}
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
                returnResult = findWord(text_list = part_word, find_word = find_word, except_word = except_word, period = period)

                '''
                if not returnResult == "":
                    #表示有找到結果
                    getInformation = returnResult
                    break
                '''
    #return getInformation 
'''
part_word =loopForCallFindWord(plantName = plantDictionary["中文名稱"], search_Param = "溫度", find_word = tempuratureText, except_word = tempuratureExceptText, period = 20)
if len(part_word) <= 0:
    for item in plantDictionary["別名"]:
        # 還在測試階段
        #part_word = loopForCallFindWord(plantName = item, search_Param = "溫度", find_word = tempuratureText, except_word = tempuratureExceptText, period = 20)
        if len(part_word) > 0:
            break
        
returnResult = callFindWord(text_list = part_word, find_word = tempuratureText, except_word = tempuratureExceptText, period = 20)
if returnResult == "":
    print("Error")
else:
    returnList["溫度"] = returnResult
    myDB.setTempurature(plantDictionary["中文名稱"], returnResult)

'''

loopForCallFindWord(plantDictionary["英文名稱"], "sun requirements", searchTextForEnglish, period = 150)
