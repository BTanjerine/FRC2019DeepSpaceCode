from wpilib.command import CommandGroup
from Command import (
    setarmpos,
    sethatchpuncherpos,
    sethatchpusherpos,
    align,
    setdrivepos
)
from wpilib.command import WaitCommand


class AutoLft(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        # self.addSequential(setdrivepos.SetDrivePos(self.robot, 0.8, 0, -900))
        # self.addSequential(WaitCommand(0.1))
        # self.addSequential(setdrivepos.SetDrivePos(self.robot, 0.8, 5000, 0))
        # self.addSequential(WaitCommand(0.1))
        # self.addSequential(setdrivepos.SetDrivePos(self.robot, 0.8, 0, -500))
        # self.addSequential(WaitCommand(0.1))
        self.addSequential(setarmpos.SetArmPos(self.robot, 0.8, 40000))
        # self.addSequential(WaitCommand(0.1))
        # self.addSequential(sethatchpuncherpos.setHatchPuncherPos(self.robot, 1))
        """
        Place hatch on near side of rocket (top), get another hatch from the hatch zone, place hatch om near side of rocket(bottom)
        """