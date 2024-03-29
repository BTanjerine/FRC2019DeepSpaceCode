from wpilib.command import Subsystem
from wpilib import SmartDashboard
from wpilib import Encoder


class Intake(Subsystem):
    def __init__(self, robot):
        super().__init__("Intake")

        self.robot = robot
        # robot map short cut
        self.map = robot.RobotMap
        # intake motors and psitons
        motor = {}
        pistons = {}

        # create all intake motors and pistons
        for name in self.map.motorMap.PWMmotor:
            motor[name] = self.robot.Creator.createPWMMotor(self.map.motorMap.PWMmotor[name])

        for name in self.map.PneumaticMap.pistons:
            if name == 'roller' or name == 'pivot':
                pistons[name] = robot.Creator.createPistons(self.map.PneumaticMap.pistons[name])

        # make motor global
        self.motor = motor
        self.pistons = pistons

        self.AngleEnc = Encoder(7, 8, False, Encoder.EncodingType.k4X)

        # set motor configs
        for name in self.motor:
            self.motor[name].setInverted(self.map.motorMap.PWMmotor[name]['inverted'])

    """
    Intake piston setters
    """
    def setIntake(self, power):
        self.motor['roller'].set(power)

    def setIntakeDeploy(self, power):
        self.motor['pivot'].set(power)
        self.motor['pivot2'].set(power)

    def setHatchPuncher(self, pos):
        self.pistons['CntPuncher'].set(pos)

    def setHatchPusher(self, pos):
        self.pistons['HatchPusher'].set(pos)

    def getSwivelEnc(self):
        return self.AngleEnc.get()

    def resetEnc(self):
        self.AngleEnc.reset()

    def log(self):
        # 650 lower
        # 0 up
        SmartDashboard.putNumber('Angle of Intake', self.getSwivelEnc())
