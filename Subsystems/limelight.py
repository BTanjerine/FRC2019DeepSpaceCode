from wpilib.command.subsystem import Subsystem
from networktables.networktables import NetworkTables


class Limelight(Subsystem):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        self.limelight = NetworkTables.getTable('limelight')

    def getXPos(self):
        """ Returns horizontal Error """
        return self.limelight.getNumber('tx', 0)

    def getYPos(self):
        """ Returns vertical Error """
        return self.limelight.getNumber('ty', 0)

    def getArea(self):
        """ Returns the percent of the screen occupied by the target """
        return self.limelight.getNumber('ta', 0)

    def setLED(self, value):
        """
        value = 0 Uses the LED mode set in the current pipeline
        value = 1 Force off
        value = 2 Force blink
        value = 3 Force on
        """
        self.limelight.putNumber('ledMode', value)

    def setCAM(self, value):
        """
        value = 0 Vision Processor
        value = 1 Driver Camera (Increases exposure, disables vision processing)
        """
        self.limelight.putNumber('camMode', value)