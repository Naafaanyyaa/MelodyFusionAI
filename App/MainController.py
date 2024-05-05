import flask
from app import song_recommender
from flask import request
import rabbitMqController


app = flask.Flask(__name__)
app.config["DEBUG"] = True


rabbitMqController.consume()


# @app.route('/api/v1/music', methods=['GET'])
# def api_all():
#
#     song_id_first = request.args['song_id_first']
#     song_id_second = request.args['song_id_second']
#
#     recommendations = song_recommender(song_id_first, song_id_second)
#
#     return recommendations.to_json(orient='records')
#
#
# app.run()
