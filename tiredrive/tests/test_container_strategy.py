from mock import Mock
from tiredrive.robot import Robot


def test_container_state_transitions():
    robot = Robot()
    robot.robotInit()
    robot.winch_encoder = Mock(robot.winch_encoder)
    robot.winch_encoder.get = Mock(return_value=-8)
    robot.winch_set = Mock()
    robot.forward = Mock()
    robot.auto_mode = "container"
    robot.autonomousInit()

    strategy = robot.strategies[robot.auto_mode]
    assert strategy.auto_state == "start"

    robot.autonomousPeriodic()
    assert strategy.auto_state == "lift"

    robot.get_winch_revs = Mock(return_value=500)
    robot.autonomousPeriodic()
    assert strategy.auto_state == "turn"
    robot.autonomousPeriodic()
    assert strategy.auto_state == "turn"

    strategy.turn_brake = Mock(return_value=True)
    robot.autonomousPeriodic()
    assert strategy.auto_state == "drive"

    strategy.positioned_count = 200
    robot.autonomousPeriodic()
    assert strategy.auto_state == "setdown"

    robot.get_winch_revs = Mock(return_value=15)
    robot.autonomousPeriodic()
    assert strategy.auto_state == "wait"

    strategy.positioned_count = 20
    robot.autonomousPeriodic()
    assert strategy.auto_state == "backup"

    strategy.positioned_count = 15
    robot.autonomousPeriodic()
    assert strategy.auto_state == "finished"
