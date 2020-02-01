from wpilib.command import Command
import enum


class ZeroArm(Command):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        self.error_count = 0

    class state(enum.IntEnum):
        Zeroing = 1
        Running = 2

    def initialize(self):
        pass

    def execute(self):
        # arm in zeroing mode resets encoder when arm is in bottom pos
        self.robot.arm.set(-0.3)
        if not self.robot.arm.getZeroPos():
            self.robot.arm.resetHeight()
            self.robot.arm.stop()
            self.error_count += 1
        else:
            self.error_count = 0

    def isFinished(self):
        # finish when arm error is close to 0
        return self.error_count > 10
        pass

    def end(self):
        # stop arm
        self.robot.arm.stop()
