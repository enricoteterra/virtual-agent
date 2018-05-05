import sys
import threading
import logging
import json
import redis
import time
from flask import Flask
from flask_socketio import SocketIO
from webdriverManager import WebDriverManager
from randomPolicyAgent import RandomPolicyAgent

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

r = redis.StrictRedis(host='localhost', port=6379)

# api routes
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(message):
    r.publish('percepts', json.dumps(message))

if __name__ == '__main__':

    webdriver = WebDriverManager(r)

    try:
        # start webserver
        webserverThread = threading.Thread(
            target=socketio.run, args=(app,))
        webserverThread.start()

        # start webdriver-simulation thread
        webdriverActThread = threading.Thread(
            target=webdriver.loop, args=(.5,))
        webdriverActThread.start()

        # agent action sequence
        time.sleep(.5)
        agent = RandomPolicyAgent(r)
        agent.publishSequence(.5, .5)

    except KeyboardInterrupt:
        sys.exit()

    except Exception as e:
            print "Error: unable to start thread - " + e.message
