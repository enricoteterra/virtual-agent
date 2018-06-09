# Semantic Grounding
teach an agent the notions of spatial representation and manipulation with the aim of developing grounded concepts that can be used in natural language. 

## Future

- multiple agents work together on shared goal 
- agents work on goal based on repeated process
- communication between agents evolves indicative, imperative and interrogative elements (see Russell)
- create a more immersive world & agents that are more closely aligned to human bodies (in terms of sensors & actuators)

## compile world

use "npm install"

use "npm run compile-vendor && npm run compile-app"

use "npm run serve"

page then becomes available at http://localhost:9615/index.html

## start agent

*note: you need to run a local redis, also install chromedriver.*

setup virtualenv and install requirements

use "python app.py"

## todo
- design & code basic interacting agent
- adjust world for goal-learning scenario
- ...