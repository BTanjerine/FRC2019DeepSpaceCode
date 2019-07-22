from wpilib.command import Command


class Align(Command):
    def __init__(self, robot, speed):
        super().__init__()
        self.robot = robot

        self.speed = speed

        self.rgt = 0
        self.lft = 0

        self.errorCounter = 0

        self.DrivePID = robot.drive.DrivePID

    def initialize(self):
        self.robot.lime.setLED(0)
        self.robot.lime.setCAM(0)
        self.robot.drive.ShiftGear(self.robot.drive.KtorqueMode)

        self.setTimeout(10000)

    def execute(self):
        turn = self.DrivePID.getOutputVal(self.speed, self.robot.lime.getXPos(), 0)

        self.rgt = turn
        self.lft = -turn

        self.robot.drive.set(self.rgt*0.2, self.lft*0.2)

        # start error count when robot is not moving
        if abs(self.rgt) <= 0.1 and abs(self.lft) <= 0.1:
            self.errorCounter += 1
        else:
            self.errorCounter = 0

    def isFinished(self):
        # finished when robot is stopped for 3 error counts
        return self.errorCounter > 5 or self.isTimedOut()

    def end(self):
        # stop arm
        self.robot.drive.stop()
        self.robot.lime.setLED(1)
        self.robot.lime.setCAM(1)
