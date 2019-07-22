from wpilib.command import Command
import enum


class SetArmPos(Command):
    def __init__(self, robot, speed, height):
        super().__init__()
        self.robot = robot

        self.mode = 1
        self.speed = speed
        self.height = height

        self.error_count = 0

    class state(enum.IntEnum):
        Zeroing = 1
        Running = 2

    def initialize(self):
        self.robot.arm.resetHeight()

    def execute(self):
        # arm in zeroing mode resets encoder when arm is in bottom pos
        if self.mode == 1:
            self.robot.arm.set(-0.1)
            if not self.robot.arm.getZeroPos():
                self.robot.arm.resetHeight()
                self.robot.arm.stop()
                self.mode = 2

        # arm in  running mode moves arm to desired position
        elif self.mode == 2:
            power = self.robot.arm.ArmPID.getOutputVal(self.speed, self.robot.arm.getHeight(), self.height)
            self.robot.arm.set(power)

            if power < 0.1:
                self.error_count += 1
            else:
                self.error_count = 0
        else:
            pass
            print("I guess do nothing")

    def isFinished(self):
        # finish when arm error is close to 0
        return self.error_count > 10
        pass

    def end(self):
        # stop arm
        self.robot.arm.stop()
