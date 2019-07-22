from ctre.wpi_talonsrx import WPI_TalonSRX
from ctre.wpi_victorspx import WPI_VictorSPX
from wpilib.victorsp import VictorSP
from wpilib.joystick import Joystick
from wpilib.xboxcontroller import XboxController
from wpilib.doublesolenoid import DoubleSolenoid
from wpilib.solenoid import Solenoid


class Creator:
    def createMotor(self, MotorSpec):
        motr = None
        if MotorSpec['ContType'] == 'CAN':
            if MotorSpec['Type'] == 'TalonSRX':
                if MotorSpec['jobType'] == 'master':
                    motr = WPI_TalonSRX(MotorSpec['port'])
                elif MotorSpec['jobType'] == 'slave':
                    motr = WPI_TalonSRX(MotorSpec['port'])
                    motr.setInverted(MotorSpec['inverted'])
                    motr.set(WPI_TalonSRX.ControlMode.Follower, MotorSpec['masterPort'])
            if MotorSpec['Type'] == 'VictorSPX':
                if MotorSpec['jobType'] == 'master':
                    motr = WPI_VictorSPX(MotorSpec['port'])
                elif MotorSpec['jobType'] == 'slave':
                    motr = WPI_VictorSPX(MotorSpec['port'])
                    motr.setInverted(MotorSpec['inverted'])
                    motr.set(WPI_VictorSPX.ControlMode.Follower, MotorSpec['masterPort'])
        else:
            print("IDK your motor")

        return motr

    def createPWMMotor(self, MotorSpec):
        if MotorSpec['Type'] == 'VictorSP':
            motr = VictorSP(MotorSpec['port'])
            motr.setInverted(MotorSpec['inverted'])
            return motr
        else:
            print("IDK your motor")

    def createPistons(self, pistonSpec):
        piston = None
        if pistonSpec['Type'] == 'Double':
            piston = DoubleSolenoid(pistonSpec['masterPort'], pistonSpec['portA'], pistonSpec['portB'])
        elif pistonSpec['Type'] == 'single':
            piston = Solenoid(pistonSpec['masterPort'], pistonSpec['portA'])
        else:
            print("IDK your pistons")
        return piston

    def createControllers(self, ConSpec):
        con = None
        if ConSpec['jobType'] == 'main':
            if ConSpec['Type'] == 'xbox':
                con = XboxController(ConSpec['Id'])
            elif ConSpec['Type'] == 'xtreme':
                con = Joystick(ConSpec['Id'])
            elif ConSpec['Type'] == 'gameCube':
                con = Joystick(ConSpec['Id'])
            else:
                print("IDK your Controller")

        elif ConSpec['jobType'] == 'side':
            if ConSpec['Type'] == 'xbox':
                con = XboxController(ConSpec['Id'])
            elif ConSpec['Type'] == 'xtreme':
                con = Joystick(ConSpec['Id'])
            elif ConSpec['Type'] == 'custom':
                con = Joystick(ConSpec['Id'])
            else:
                print("IDK your Controller")

        else:
            print("IDK your Controller")

        return con
