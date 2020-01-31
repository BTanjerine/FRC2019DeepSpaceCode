from wpilib.command import CommandGroup


class Autolvl2Lft(CommandGroup):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot
        """
        Place hatch on near side of rocket (top), get another hatch from the hatch zone, place hatch om near side of rocket(bottom)
        """