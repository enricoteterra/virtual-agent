import unittest
from app.domain.robot.Robot import Robot


class AppTest(unittest.TestCase):
    def test_robot_performs_task(self):
        robot = Robot()
        finalState = robot.performTask()
        expectedState = True
        self.assertEqual(expectedState, finalState)
