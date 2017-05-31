from flask import Flask, jsonify
from flask import url_for, redirect
from flask import request, abort, make_response
import json
from flask_cors import CORS
import datetime
from mainFile import main
app = Flask(__name__)
from CONSTANTS import file_constants

currState = "Mymanual"
currMsg = ""
CORS(app)

@app.route('/auth', methods=['GET'])
# @auth.login_required
def get_auth():
    global currMsg, currState
    dialogue = "Hello. I am your Sonicare expert. How can I help you?"
    currState = file_constants.myConstants.initialState
    # response = Response(dialogue, content_type='application/json; charset=utf-8')
    # response.headers.add('content-length', len(dialogue))
    # response.status_code = 200
    return jsonify(dialogue),200

@app.route('/auth', methods=['POST'])
# @auth.login_required
def post_auth():
    global currState, currMsg
    ut=request.json['dialogue']
    if ut.lower() in file_constants.myConstants.salutation_messages:
        return "Nice to meet you. How may I help you"
    currMsg, currState, currScore = main.sent_answer(ut,currState)
    # return ut+str(datetime.datetime.now())
    return currMsg

if __name__ == "__main__":
    app.run(host='localhost',port = 9004)