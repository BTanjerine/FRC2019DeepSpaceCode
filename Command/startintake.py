from wpilib.command import Command


class StartIntake(Command):
    def __init__(self, robot, speed, time):
        super().__init__()
        self.robot = robot

        # set speed and timer
        self.speed = speed
        self.time = time

    def initialize(self):
        # start time out
        self.setTimeout(self.time)

    def execute(self):
        # start intake
        self.robot.intake.setIntake(self.speed)

    def isFinished(self):
        return self.isTimedOut()

    def end(self):
        # stop intake
        self.robot.intake.set_intake(0)