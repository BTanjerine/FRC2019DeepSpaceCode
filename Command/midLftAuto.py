from wpilib.command import CommandGroup


class AutoMidLft(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        """
        Place hatch on hab, get another hatch
        """