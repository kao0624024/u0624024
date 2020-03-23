import myString


nameDB = myString.getNameDB() 
phDB = myString.getPhDB()
moistureDB = myString.getMoistureDB()
tempuratureDB = myString.getTempuratureDB()
sunlightDB = myString.getSunlightDB()

ChineseName = myString.getPlantCName()
EnglishName = myString.getPlantEName()
ScientificName = myString.getPlantSName()
Order = myString.getPlantOrder()
OtherName = myString.getPlantOName()

def getPlantName(plantName, fileName = nameDB):
    #要回傳的
    plantDictionary = {ChineseName : [],
                    EnglishName : [],
                    ScientificName : [],
                    Order : [],
                    OtherName : []}
    #方便讀取字典
    titleStrings = ["中文名稱", "英文名稱", "學名", "科名", "別名", "只是防止出錯用的"]
    dictionaryString = [ChineseName, EnglishName, ScientificName, Order, OtherName]
    f = open(fileName, "r")
    nameList = f.read()
    nameList = nameList.split("\n")
    #用來記錄優先度的list，如：有中文名稱一樣的為主，而別名相同的優先度再後
    returnList = []
    for name in nameList:
        #csv以逗號分隔
        checkList = name.split(",")
        for index, check in enumerate(checkList):
            if check.find(plantName) > -1:
                #有找到，第一個為找到的位置數值，第二為內容
                returnList.append(index)
                returnList.append(name)
    f.close()
    #表示沒找到，長度才會等於0
    if len(returnList) == 0:
        return plantDictionary
    priority = 0
    for index in range(len(returnList)):
        #0,2,4...為數值(優先度)，1,3,5為對應的內容
        if not index / 2 == 0:
            continue
        #數值越小表示越先找到對應的值，而中文名稱為最前面，藉此判斷優先度
        if priority < returnList[index]:
            priority = index
    index = 0
    itemList = returnList[priority + 1].split(",")
    for addItem in itemList:
        if addItem == titleStrings[0] : continue
        if addItem == titleStrings[index + 1]:
            index = index + 1
            continue
        plantDictionary[dictionaryString[index]].append(addItem)
    #主程式的中文名稱是用String
    plantDictionary[ChineseName] = str(plantDictionary[ChineseName][0])
    return plantDictionary


def setPlantName(plantDictionary, fileName = nameDB):
    titleStrings = ["中文名稱", "英文名稱", "學名", "科名", "別名", "只是防止出錯用的"]
    dictionaryString = [ChineseName, EnglishName, ScientificName, Order, OtherName]
    writeInDB = "中文名稱," + plantDictionary[ChineseName] + ","
    for index in range(1, len(titleStrings)):
        if index == len(titleStrings) - 1:
            #表示已經跑完
            writeInDB = writeInDB[:-1]
            writeInDB = writeInDB + "\n"
            break
        writeInDB = writeInDB + titleStrings[index] + ","
        for item in plantDictionary[dictionaryString[index]]:
            writeInDB = writeInDB + item + ","
    f = open(fileName, "a")
    f.write(writeInDB)
    f.close()
    

def getPh(plantName, fileName = phDB):
    f = open(fileName, "r")
    phList = f.read()
    phList = phList.split("\n")
    for ph in phList:
        check = ph.split(",")
        for plant in plantName:
            if check[0].lower().find(plant.lower()) > -1:
                return(check[1])
    f.close()
    return("")


def setPh(plantName, phValue, fileName = phDB):
    writeInDB = plantName + "," + phValue + "\n"
    f = open(fileName, "a")
    f.write(writeInDB)
    f.close()


def getMoisture(plantName, fileName = moistureDB):
    f = open(fileName, "r")
    moistureList = f.read()
    moistureList = moistureList.split("\n")
    for moisture in moistureList:
        check = moisture.split(",")
        for plant in plantName:
            if check[0].lower().find(plant.lower()) > -1:
                return(check[1])
    f.close()
    return("")


def setMoisture(plantName, moistureValue, fileName = moistureDB):
    writeInDB = plantName + "," + moistureValue + "\n"
    f = open(fileName, "a")
    f.write(writeInDB)
    f.close()


def getTempurature(plantName, fileName = tempuratureDB):
    f = open(fileName, "r")
    tempuratureList = f.read()
    tempuratureList = tempuratureList.split("\n")
    for tempurature in tempuratureList:
        check = tempurature.split(",")
        if check[0].lower().find(plantName.lower()) > -1:
            return(check[1])
    f.close()
    return("")


def setTempurature(plantName, tempuratureValue, fileName = tempuratureDB):
    writeInDB = plantName + "," + tempuratureValue + ",℃\n"
    f = open(fileName, "a")
    f.write(writeInDB)
    f.close()


def getSunlight(plantName, fileName = sunlightDB):
    f = open(fileName, "r")
    sunlightList = f.read()
    sunlightList = sunlightList.split("\n")
    for sunlight in sunlightList:
        check = sunlight.split(",")
        for thePlant in plantName:
            if check[0].lower().find(thePlant.lower()) > -1:
                return(check[1])
    f.close()
    return("")


def setSunlight(plantName, sunlightValue, fileName = sunlightDB):
    writeInDB = plantName + "," + sunlightValue + "\n"
    f = open(fileName, "a")
    f.write(writeInDB)
    f.close()


if __name__ == "__main__":
    getSunlight("百日草")

