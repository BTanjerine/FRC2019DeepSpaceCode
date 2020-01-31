import wpilib
from wpilib import SmartDashboard
from commandbased import CommandBasedRobot
from wpilib.command import Scheduler

from Subsystems.drive import Drive
from Subsystems.arm import Arm
from Subsystems.intake import Intake
from Subsystems.limelight import Limelight

from Command.teleop import TeleOp
from Command import (
    lftauto,
    Lvl2lftAuto,
    Lvl2rgtAuto,
    rgtauto,
    midRgtAuto,
    midLftAuto,
)

from robotMap import RobotMap
from Helper import Creator
from OI import oi

class Robot(CommandBasedRobot):

    TestVar = 0

    def robotInit(self):
        super().__init__()
        # init robot subs and commands
        self.RobotMap = RobotMap(self)  # map of the robot body
        self.Creator = Creator()    # program to create robot parts for subs

        "******************robot subsystems**********************"
        self.arm = Arm(self)    # arm subsystem
        self.drive = Drive(self)    # drive subsystem
        self.intake = Intake(self)  # intake subsystem
        self.lime = Limelight(self)     # limelight camera subsystem
        self.OI = oi(self)      # joystick controller program

        "**********************robot autons and user control*********************"
        self.teleOp = TeleOp(self)

        self.autoLft = lftauto.AutoLft(self)
        self.autoRgt = rgtauto.AutoRgt(self)
        self.autoMidRgt = midRgtAuto.AutoMidRgt(self)
        self.autoMidLft = midLftAuto.AutoMidLft(self)
        self.autoLvl2Rgt = Lvl2rgtAuto.Autolvl2Rgt(self)
        self.autoLvl2Lft = Lvl2lftAuto.Autolvl2Lft(self)

        "************************autonomous chooser****************************"
        self.selectedAuto = self.autoLft

        self.s = Scheduler

    def robotPeriodic(self):
        self.s.getInstance().run()  # run auto

    def log(self):
        self.drive.Log()    # log drive data
        self.arm.log()      # log arm data

    def autonomousInit(self):
        # choose auto program
        self.selectedAuto.cancel()
        self.selectedAuto = self.chooser.getSelected()  # find what auto was selected
        self.selectedAuto.start()   # start chosen auto

    def autonomousPeriodic(self):
        # cut auto if fail and go to driver
        if self.OI.getMainController().getStartButton():
            self.selectedAuto.cancel()
            self.selectedAuto = self.teleOp
            self.selectedAuto.start()

        # self.s.getInstance().run()   # run auto
        self.log()  # log important data on to smartdashboard

    def teleopInit(self):
        # stops old auto and goes to teleop
        self.selectedAuto.cancel()
        self.teleOp.start()     # start teleop

    def teleopPeriodic(self):
        self.log()  # log important data on to smartdashboard

    def disabledInit(self):
        pass  # nothing

    def disabledPeriodic(self):
        self.log()  # log important data on to smartdashboard


if __name__ == '__main__':
    wpilib.run(Robot)
