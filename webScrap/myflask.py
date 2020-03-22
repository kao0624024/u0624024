import flask
app = flask.Flask(__name__)
import webScraping as web


@app.route("/plant/<plantName>")
def getPlant(plantName):
    info = web.webScrap(plantName = plantName)
    return info
    #return plantName

@app.route("/")
def home():
    return "hello"

if __name__ == "__main__":
    app.debug = False 
    app.run(host = "0.0.0.0")
