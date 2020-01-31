import wpilib
from wpilib import DoubleSolenoid
from wpilib.command import Subsystem
from wpilib import Encoder
from wpilib import ADXRS450_Gyro
from Subsystems.pid import PID
import hal


class Drive(Subsystem):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        self.peakCurrentLimit = 25
        self.PeaKDuration = 50
        self.continuousLimit = 15

        self.map = robot.RobotMap

        # drive motor, sensors, and pistons
        motor = {}
        pistons = {}

        # create all drive motors, Sensors, and pistons
        for name in self.map.motorMap.motors:
            motor[name] = robot.Creator.createMotor(self.map.motorMap.motors[name])

        for name in self.map.PneumaticMap.pistons:
            if name == 'Shifter':
                pistons[name] = robot.Creator.createPistons(self.map.PneumaticMap.pistons[name])

        self.REnc = Encoder(0, 1, True, Encoder.EncodingType.k4X)
        self.LEnc = Encoder(2, 3, False, Encoder.EncodingType.k4X)

        self.Gyro = ADXRS450_Gyro()

        # make motors, Sensors, and pistons local to subsystem
        self.Dmotor = motor
        self.Dpiston = pistons

        for name in self.Dmotor:
            self.Dmotor[name].setInverted(self.robot.RobotMap.motorMap.motors[name]['inverted'])

            # drive current limit
            self.Dmotor[name].configPeakCurrentLimit(self.peakCurrentLimit, 10)
            self.Dmotor[name].configPeakCurrentDuration(self.PeaKDuration, 10)
            self.Dmotor[name].configContinuousCurrentLimit(self.continuousLimit, 10)
            self.Dmotor[name].enableCurrentLimit(True)

        self.KtorqueMode = DoubleSolenoid.Value.kReverse
        self.KspeedMode = DoubleSolenoid.Value.kForward

        if hal.isSimulation():
            self.kp = 0.001
            self.ki = 0.00001
            self.kd = 0.000000001
        else:
            self.kp = 0.001
            self.ki = 0.00001
            self.kd = 0.000000001

        self.DrivePID = PID(self.kp, self.ki, self.kd)

    def Log(self):
        wpilib.SmartDashboard.putNumber('rgt enc', self.REnc.get())
        wpilib.SmartDashboard.putNumber('lft enc', self.LEnc.get())

        wpilib.SmartDashboard.putNumber('drive rgt frt', self.Dmotor['RFDrive'].getOutputCurrent())
        wpilib.SmartDashboard.putNumber('drive lft frt', self.Dmotor['LFDrive'].getOutputCurrent())

    """
    Get Functions
    """
    def getEncoderVal(self):
        # get encoder values from both sides
        rgt = self.REnc.get()
        lft = self.LEnc.get()
        avg = (rgt+lft)/2   # find average
        return avg

    def getGyroVal(self):
        # get gyro values
        x = self.Gyro.getAngle()
        # reset gyro if it passes 360 deg
        if x > 360 or x < -360:
            self.resetGyro()
        return self.Gyro.getAngle()

    """
    Set Functions
    """
    def set(self, rgt, lft):
        self.Dmotor['RFDrive'].set(self.Dmotor['RFDrive'].ControlMode.PercentOutput, rgt)
        self.Dmotor['LFDrive'].set(self.Dmotor['LFDrive'].ControlMode.PercentOutput, lft)

        # uncomment when all motors are master
        """self.Dmotor['RMDrive'].set(self.Dmotor['RMDrive'].ControlMode.PercentOutput, rgt)
        self.Dmotor['RBDrive'].set(self.Dmotor['RBDrive'].ControlMode.PercentOutput, rgt)"""

        """self.Dmotor['LMDrive'].set(self.Dmotor['LMDrive'].ControlMode.PercentOutput, lft)
        self.Dmotor['LBDrive'].set(self.Dmotor['LBDrive'].ControlMode.PercentOutput, lft)"""

    def stop(self):
        self.set(0, 0)

    def ShiftGear(self, GearMode):
        self.Dpiston['Shifter'].set(GearMode)

    def resetEnc(self):
        self.REnc.reset()
        self.LEnc.reset()

    def resetGyro(self):
        self.Gyro.reset()

