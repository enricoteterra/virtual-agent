import sys
import time
import threading
import logging
import redis
from flask import Flask
from flask_socketio import SocketIO
from simpleReflexAgent import SimpleReflexAgent

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

r = redis.StrictRedis(host='localhost', port=6379)

# api routes
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(message):
    print message
    r.publish('percepts', message)

if __name__ == '__main__':

    agent = SimpleReflexAgent(r)

    try:
        # start webserver
        webserverThread = threading.Thread(
            target=socketio.run, args=(app,))
        webserverThread.start()

        # start simulation & agent threads
        agentScreencaptureThread = threading.Thread(target=agent.screencaptureLoop)
        agentScreencaptureThread.start()

        agentActThread = threading.Thread(target=agent.actLoop)
        agentActThread.start()

    except KeyboardInterrupt:
        sys.exit()

    except Exception as e:
            print "Error: unable to start thread - " + e.message
