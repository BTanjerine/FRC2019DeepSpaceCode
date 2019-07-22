import wpilib


class RobotMap:
    def __init__(self, robot):
        self.robot = robot
        self.motorMap = MotorMap()
        self.PneumaticMap = PneumaticMap()
        self.ControlMap = ControlMap()


class MotorMap:
    def __init__(self):
        self.motors = {}
        self.PWMmotor = {}

        """
        Drive Motors
        """
        self.motors['RFDrive'] = {
            'port': 1,
            'inverted': True,
            'jobType': 'master',
            'ContType': 'CAN',
            'Type': 'TalonSRX'}

        self.motors['RMDrive'] = {
            'port': 4,
            'inverted': True,
            'jobType': 'slave',
            'masterPort': 1,
            'ContType': 'CAN',
            'Type': 'TalonSRX'}
        self.motors['RBDrive'] = {
            'port': 7,
            'inverted': True,
            'jobType': 'slave',
            'masterPort': 1,
            'ContType': 'CAN',
            'Type': 'TalonSRX'}

        self.motors['LFDrive'] = {
            'port': 9,
            'inverted': False,
            'jobType': 'master',
            'ContType': 'CAN',
            'Type': 'TalonSRX'}
        self.motors['LMDrive'] = {
            'port': 0,
            'inverted': False,
            'jobType': 'slave',
            'masterPort': 9,
            'ContType': 'CAN',
            'Type': 'TalonSRX'}
        self.motors['LBDrive'] = {
            'port': 2,
            'inverted': False,
            'jobType': 'slave',
            'masterPort': 9,
            'ContType': 'CAN',
            'Type': 'TalonSRX'}

        """
        Arm Motors
        """
        self.motors['RTArm'] = {
            'port': 3,
            'inverted': False,
            'jobType': 'master',
            'ContType': 'CAN',
            'Type': 'TalonSRX'}
        self.motors['RBArm'] = {
            'port': 5,
            'inverted': True,
            'jobType': 'slave',
            'masterPort': 3,
            'ContType': 'CAN',
            'Type': 'TalonSRX'}
        self.motors['LTArm'] = {
            'port': 6,
            'inverted': True,
            'jobType': 'master',
            'ContType': 'CAN',
            'Type': 'TalonSRX'}
        self.motors['LBArm'] = {
            'port': 8,
            'inverted': True,
            'jobType': 'slave',
            'masterPort': 6,
            'ContType': 'CAN',
            'Type': 'TalonSRX'}

        """
        Intake motors
        """
        self.PWMmotor['roller'] = {'port': 8, 'inverted': True, 'ContType': 'PWM', 'Type': 'VictorSP'}
        self.PWMmotor['pivot'] = {'port': 9, 'inverted': False, 'ContType': 'PWM', 'Type': 'VictorSP'}


class PneumaticMap:
    def __init__(self):
        self.pistons = {}

        self.OUT = wpilib.DoubleSolenoid.Value.kForward
        self.IN = wpilib.DoubleSolenoid.Value.kReverse
        self.CLOSE = wpilib.DoubleSolenoid.Value.kOff

        """
        Drive Pistons
        """
        self.pistons['Shifter'] = {'portA': 0, 'portB': 1, 'Type': 'Double', 'masterPort': 0}

        """
        Intake Pistons
        """
        self.pistons['HatchPusher'] = {'portA': 1, 'portB': 2, 'Type': 'Double', 'masterPort': 0}
        self.pistons['CntPuncher'] = {'portA': 3, 'portB': 4, 'Type': 'Double', 'masterPort': 0}


class ControlMap:
    def __init__(self):
        self.Controller = {}

        """
        drive controller
        """
        self.Controller['xbox'] = {'Id': 0, 'Type': 'xbox', 'jobType': 'main'}

        """
        Extra controller for controlling arm 
        """
        self.Controller['board'] = {'Id': 1, 'Type': 'custom', 'jobType': 'side'}
