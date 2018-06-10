import unittest
import jsonschema
import json
import redislite
from app.agents import RandomPolicyAgent

class RandomPolicyAgentTest(unittest.TestCase):
        
    def setUp(self):
        self.mockRedis = redislite.StrictRedis()
        self.agent = RandomPolicyAgent(self.mockRedis)

        self.actionSchema = {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "lookLeft",
                        "lookUp",
                        "lookRight",
                        "lookDown",
                        "moveLeft",
                        "moveForward",
                        "moveRight",
                        "moveBack"
                    ]
                },
                "actuator": {
                    "type": "string",
                    "enum": ["look", "move"]
                },
                "direction" : {
                    "type": "string",
                    "enum": ["left", "up", "right", "down", "back", "forward"]
                },
                "factor": {
                    "type" : "number"
                }
            },
            "required": ["action", "actuator", "direction", "factor"]
        }

        self.actionSequenceSchema = {
            "type": "object",
            "properties": {
                "actions": {
                    "type": "array",
                    "items": self.actionSchema,
                    "additionalItems": False
                }
            }
        }


    def test_generateActionSequence_ManySteps(self):
        """
        test that agent generates a valid action sequence.
        """

        result = self.agent.generateActionSequence(
            steps=10,
            baseMovementFactor=1.0)

        jsonschema.validate(
            result, 
            self.actionSequenceSchema)

        self.assertTrue(len(result["actions"]) == 10)


    def test_generateActionSequence_OneStep(self):
        """
        test that agent generates a valid action sequence.
        """

        result = self.agent.generateActionSequence(
            steps=1,
            baseMovementFactor=1.0)

        jsonschema.validate(
            result, 
            self.actionSequenceSchema)

        self.assertTrue(len(result["actions"]) == 1)


    def test_publishSequence_singleStep(self):
        """
        test that action sequence is published to queue.
        """

        sub = self.mockRedis.pubsub()
        sub.subscribe('actions')  

        msg = sub.get_message()
        self.assertTrue(msg["data"] == 1L)

        self.agent.publishSequence(baseMovementFactor=1.0, stepsPerIteration=1)

        msg = sub.get_message()
        jsonschema.validate(
            json.loads(msg["data"]), 
            self.actionSequenceSchema)

        msg = sub.get_message()
        self.assertIsNone(msg)

    def test_publishSequence_manySteps(self):
        """
        test that action sequence is published to queue.
        """

        sub = self.mockRedis.pubsub()
        sub.subscribe('actions')  

        msg = sub.get_message()
        self.assertTrue(msg["data"] == 1L)

        self.agent.publishSequence(baseMovementFactor=1.0, stepsPerIteration=10)

        msg = sub.get_message()
        jsonschema.validate(
            json.loads(msg["data"]), 
            self.actionSequenceSchema)

        msg = sub.get_message()
        self.assertIsNone(msg)


if __name__ == '__main__':
    unittest.main()
