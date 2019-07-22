from wpilib.command.commandgroup import CommandGroup
from Command import (
    setarmpos,
    sethatchpuncherpos,
    sethatchpusherpos,
    align,
    setdrivepos
)
from wpilib.command.waitcommand import WaitCommand


class AutoMidRgt(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        """
        Place hatch on hab, get another hatch
        """
        self.addSequential(setdrivepos.SetDrivePos(robot, 0.2, 1000, 0))
        self.addParallel(setarmpos.SetArmPos(robot, 0.8, 4000))
        self.addSequential(WaitCommand(0.3))
        self.addSequential(setarmpos.SetArmPos(robot, 0.8, 13000))
