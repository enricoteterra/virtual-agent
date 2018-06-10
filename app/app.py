"""
Virtual Env Backend Service.

runs socketio web server, chrome webdriver & agent.

- agent & webdriver communicate via redis pub/sub.
- webdriver & browser communicate via selenium & socket connection.
"""

import sys
import threading
import logging
import json
import redis
from flask import Flask
from flask_socketio import SocketIO
from webdriver.webdriverManager import WebDriverManager
from agents.randomPolicyAgent import RandomPolicyAgent

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

r = redis.StrictRedis(host='localhost', port=6379)

# api route definition
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(message):
    r.publish('percepts', json.dumps(message))

# start server
if __name__ == '__main__':

    webdriver = WebDriverManager(r)

    try:
        # start webserver
        webserverThread = threading.Thread(
            target=socketio.run, args=(app,))
        webserverThread.daemon = True
        webserverThread.start()

        # start webdriver-simulation thread
        webdriverActThread = threading.Thread(
            target=webdriver.loop, args=(.1,))
        webdriverActThread.daemon = True
        webdriverActThread.start()

        # agent action sequence
        agent = RandomPolicyAgent(r)
        agent.publishSequenceLoop(
            publishFrequency=.1,
            baseMovementFactor=.2,
            stepsPerIteration=1)

    except (KeyboardInterrupt, SystemExit):
        sys.exit()

    except Exception as e:
            print "Error: unable to start app - " + e.message
