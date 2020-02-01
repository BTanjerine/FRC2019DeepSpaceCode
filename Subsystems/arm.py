from ctre import WPI_TalonSRX
from ctre import WPI_VictorSPX
from wpilib.command import Subsystem
from Subsystems.pid import PID
from wpilib import Encoder
from wpilib import DigitalInput
import wpilib
import ctre

class Arm(Subsystem):
    def __init__(self, robot):
        super().__init__("Arm")
        self.robot = robot

        self.peakCurrentLimit = 30
        self.PeaKDuration = 50
        self.continuousLimit = 15

        motor = {}

        for name in self.robot.RobotMap.motorMap.motors:
            motor[name] = self.robot.Creator.createMotor(self.robot.RobotMap.motorMap.motors[name])

        self.motors = motor

        for name in self.motors:
            self.motors[name].setInverted(self.robot.RobotMap.motorMap.motors[name]['inverted'])
            # drive current limit
            self.motors[name].configPeakCurrentLimit(self.peakCurrentLimit, 10)
            self.motors[name].configPeakCurrentDuration(self.PeaKDuration, 10)
            self.motors[name].configContinuousCurrentLimit(self.continuousLimit, 10)
            self.motors[name].enableCurrentLimit(True)

        self.AEnc = Encoder(4, 5, False, Encoder.EncodingType.k4X)
        self.Zero = DigitalInput(6)

        self.kp = 0.00035
        self.ki = 0.00000000001
        self.kd = 0.0000001

        self.ArmPID = PID(self.kp, self.ki, self.kd)

    def log(self):
        wpilib.SmartDashboard.putNumber('armEnc', self.getHeight())
        wpilib.SmartDashboard.putNumber('Zero', self.getZeroPos())

    """
    Get Functions
    """

    def getHeight(self):
        # get encoder values
        return self.AEnc.get()

    def getZeroPos(self):
        # get zero position of arm
        return self.Zero.get()

    """
    set functions
    """
    def set(self, power):
        self.motors['RTArm'].set(ctre.ControlMode.PercentOutput, power)
        self.motors['LTArm'].set(ctre.ControlMode.PercentOutput, power)

    def stop(self):
        self.set(0)

    def resetHeight(self):
        self.AEnc.reset()
