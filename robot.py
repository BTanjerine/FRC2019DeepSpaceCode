import wpilib
from wpilib.command import Scheduler
from wpilib.sendablechooser import SendableChooser
from commandbased import CommandBasedRobot

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
        self.chooser = SendableChooser()

        self.chooser.setDefaultOption("Drive Mode", self.teleOp)
        self.chooser.addOption("Auto Left", self.autoLft)
        self.chooser.addOption("Auto Mid Rgt", self.autoMidRgt)
        self.chooser.addOption("Auto Mid Lft", self.autoMidLft)
        self.chooser.addOption("Auto Right", self.autoRgt)

        self.chooser.addOption("Auto Lvl2 Rgt", self.autoLvl2Rgt)
        self.chooser.addOption("Auto Lvl2 Lft", self.autoLvl2Lft)
        wpilib.SmartDashboard.putData('Options', self.chooser)

        self.selectedAuto = self.chooser.getSelected()

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

        Scheduler.getInstance().run()   # run auto
        self.log()  # log important data on to smartdashboard

    def teleopInit(self):
        # stops old auto and goes to teleop
        self.selectedAuto.cancel()
        self.teleOp.start()     # start teleop

    def teleopPeriodic(self):
        Scheduler.getInstance().run()  # run auto
        self.log()  # log important data on to smartdashboard

    def disabledInit(self):
        pass  # nothing

    def disabledPeriodic(self):
        self.log()  # log important data on to smartdashboard


if __name__ == '__main__':
    wpilib.run(Robot)
