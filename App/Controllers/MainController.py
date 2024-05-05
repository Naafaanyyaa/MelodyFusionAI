import flask
import rabbitMqController

app = flask.Flask(__name__)
app.config["DEBUG"] = True

rabbitMqController.consume()