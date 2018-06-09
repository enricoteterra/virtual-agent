# Semantic Grounding
teach an agent the notions of spatial representation and manipulation with the aim of developing grounded concept models that can be used to better interpret natural language. 

## Future

- multiple agents work together on shared goal 
- agents work on goal based on repeated process
- communication between agents evolves indicative, imperative and interrogative elements (see Russell)
- create a more immersive world & agents that are more closely aligned to human bodies (in terms of sensors & actuators)

## compile & run world

use "npm install"

use "npm run compile-vendor && npm run compile-app"

use "npm run serve"

virtual environment served at http://localhost:9615/index.html

## start agent

*note: you need to run a local redis, which is used as microservice glue.*

setup virtualenv and install requirements: 

use "source env/bin/activate"

use "pip install -r requirements.txt"

use "python app/app.py"

## todo
- unit tests python webdriver and agents
- design & code dqn & gan agents based on papers
- ...