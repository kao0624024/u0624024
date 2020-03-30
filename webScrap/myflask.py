import flask
app = flask.Flask(__name__)
import main 


@app.route("/plant/<plantName>")
def getPlant(plantName):
    info = main.webScrap(plantName = plantName)
    return info
    #return plantName

@app.route("/")
def home():
    return "hello"

if __name__ == "__main__":
    app.debug = False 
    app.run(host = "0.0.0.0")
