from wpilib.command import Command
import hal


class SetDrivePos(Command):
    def __init__(self, robot, speed, distance, turnDegree):
        super().__init__()
        self.robot = robot

        # drive percent output
        self.speed = speed

        # drive linear distance
        if hal.isSimulation():
            # change distance bc its different in simulation
            self.distance = distance/2
        else:
            self.distance = distance

        # drive turning degree
        self.turnDegree = turnDegree

        # drive percent output
        self.rgt = 0
        self.lft = 0

        self.errorCounter = 0

        self.DrivePID = robot.drive.DrivePID

        self.robot.drive.resetEnc()
        self.robot.drive.resetGyro()

    def initialize(self):
        self.robot.drive.resetEnc()
        self.robot.drive.resetGyro()

    def execute(self):
        lin = self.DrivePID.getOutputVal(self.speed, -self.robot.drive.getEncoderVal(), self.distance)
        turn = -self.DrivePID.getOutputVal(self.speed, self.robot.drive.getGyroVal(), self.turnDegree)

        # if only linear motion
        if self.distance != 0 and self.turnDegree == 0:
            self.rgt = lin
            self.lft = lin
        # if only turn motion
        elif self.distance == 0 and self.turnDegree != 0:
            self.rgt = -turn
            self.lft = turn
        # if swerve motion
        elif self.distance != 0 and self.turnDegree != 0:
            self.rgt = lin - turn
            self.lft = lin + turn

        # set percent output to drive
        self.robot.drive.set(self.rgt, self.lft)

        # start error count when robot is not moving
        if abs(self.rgt) <= 0.1 and abs(self.lft) <= 0.1:
            self.errorCounter += 1
        else:
            self.errorCounter = 0

    def isFinished(self):
        # finished when robot is stopped for 3 error counts
        return self.errorCounter > 10

    def end(self):
        # stop arm
        self.robot.drive.resetEnc()
        self.robot.drive.resetGyro()
        self.robot.drive.stop()
