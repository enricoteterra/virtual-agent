#!/usr/bin/python

import threading
from flask import Flask
from flask_socketio import SocketIO
from simpleReflexAgent import SimpleReflexAgent

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

if __name__ == '__main__':

    agent = SimpleReflexAgent()

    try:
        webserverThread = threading.Thread(
            target=socketio.run, args=(app,))
        webserverThread.start()

        agentThread = threading.Thread(target=agent.loop)
        agentThread.start()

    except:
        print "Error: unable to start thread"