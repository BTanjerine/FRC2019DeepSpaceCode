from wpilib.command import Command
import enum
import wpilib.doublesolenoid


class setHatchPuncherPos(Command):
    def __init__(self, robot, pos):
        super().__init__()
        self.robot = robot

        # set speed and timer
        self.pos = pos

    class Pos(enum.IntEnum):
        Out = 1
        In = 2

    def initialize(self):
        # start time out
        self.setTimeout(0.5)

    def execute(self):
        # start intake
        if self.pos == self.Pos.Out:
            self.robot.intake.setHatchPuncher(wpilib.DoubleSolenoid.Value.kForward)
        elif self.pos == self.Pos.In:
            self.robot.intake.setHatchPuncher(wpilib.DoubleSolenoid.Value.kReverse)

    def isFinished(self):
        return self.isTimedOut()