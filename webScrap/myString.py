nameDB = r"myDB\name.csv"
phDB = r"myDB\ph.csv"
moistureDB = r"myDB\moisture.csv"
tempuratureDB = r"myDB\tempurature.csv"
sunlightDB = r"myDB\sunlight.csv"
dictionaryName = {"中文名稱": "chineseName", "英文名稱":"englishName", "學名":"scientificName", "科名":"order", "別名":"otherName"}
dictionaryInformation = {"溫度":"tempurature", "濕度":"soil moisture", "ph值":"pH value", "日照":"sun light"}
titleStrings = ["中文名稱", "英文名稱", "學名", "科名", ["別名", "別稱"], "只是防止出錯用的"]


def getNameDB():
    return nameDB


def getPhDB():
    return phDB


def getMoistureDB():
    return moistureDB


def getTempuratureDB():
    return tempuratureDB


def getSunlightDB():
    return sunlightDB


def getPlantCName():
    return dictionaryName["中文名稱"]


def getPlantEName():
    return dictionaryName["英文名稱"]


def getPlantSName():
    return dictionaryName["學名"]


def getPlantOrder():
    return dictionaryName["科名"]


def getPlantOName():
    return dictionaryName["別名"]


def getTempuratureName():
    return dictionaryInformation["溫度"]


def getMoistureName():
    return dictionaryInformation["濕度"]


def getPhName():
    return dictionaryInformation["ph值"]


def getSunlightName():
    return dictionaryInformation["日照"]


def getTitleStrings():
    return titleStrings


if __name__ == "__main__":
    print(nameDB)
