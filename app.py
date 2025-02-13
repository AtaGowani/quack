from classifier import clf
from flask import Flask, render_template, jsonify, request, json
from hand_data import get_hand_position
from lib import Leap
import pickle
import random
import redis

app = Flask(__name__)

controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

past_symbol = 'a'
prev_prediction = None

r = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/')
def home():
    return render_template('splash.html')

@app.route('/translate')
def translate():
    return render_template('ui.html')

# @app.route('/tutorial')
# def tutorial():
#     return render_template('tutorial.html')

@app.route('/game1')
def game1():
    return render_template('game1.html')

@app.route('/game2')
def game2():
    return render_template('index.html')

@app.route('/score', methods=['POST'])
def add_score():
    data = request.form
    try:
        record = json.dumps({'user': data['user'], 'score': int(data['score'])})
        print record
        result = r.lpush('scoreboard', record)
        return jsonify(error=result)
    except KeyError:
        return jsonify(error=True)

@app.route('/scores', methods=['GET'])
def get_scores():
    scores = [json.loads(i) for i in r.lrange('scoreboard', 0, 100)]
    scores.sort(key=lambda s: s['score'], reverse=True)
    return jsonify(scores=scores[:10])

# # Keeping scores for game 3
# @app.route('/score3', methods=['POST'])
# def add_score3():
#     data = request.form
#     try:
#         record = json.dumps({'user': data['user'], 'score': int(data['score'])})
#         print record
#         result = r.lpush('scoreboard3', record)
#         return jsonify(error=result)
#     except KeyError:
#         return jsonify(error=True)

# @app.route('/scores3', methods=['GET'])
# def get_scores3():
#     scores3 = [json.loads(i) for i in r.lrange('scoreboard3', 0, 100)]
#     scores3.sort(key=lambda s: s['score'], reverse=True)
#     return jsonify(scores3=scores3[:10])


@app.route('/current')
def current_symbol():
    global past_symbol
    global prev_prediction

    # Is there a hand?
    hand_pos = get_hand_position(controller)
    if not hand_pos:
        new = past_symbol != ' '
        past_symbol = ' '
        return jsonify(symbol=' ', new=new)
    features = [v for k, v in hand_pos.iteritems()]

    # Do we have a new symbol?
    prediction = ''.join(clf.predict(features))
    if prediction == prev_prediction:
        # We good fam
        return jsonify(new=False, symbol=prediction)
    else:
        prev_prediction = prediction
        return jsonify(new=True, symbol=prediction)

@app.route('/splash')
def splash():
    return render_template('splash.html')


@app.route('/scoreboard')
def scoreboard():
    return jsonify(user_score=100)

# @app.route('/scoreboard3')
# def scoreboard3():
#     return jsonify(user_score=100)

if __name__ == '__main__':
    app.run(debug=True)
