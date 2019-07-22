from wpilib.buttons.joystickbutton import JoystickButton
from Command import (
    setarmpos,
    sethatchpuncherpos,
    sethatchpusherpos,
    align
)


class oi(object):
    def __init__(self, robot):
        super().__init__()

        self.robot = robot
        MainCon = {}
        SideCon = {}

        for name in robot.RobotMap.ControlMap.Controller:
            if robot.RobotMap.ControlMap.Controller[name]['jobType'] == 'main':
                MainCon[name] = robot.Creator.createControllers(robot.RobotMap.ControlMap.Controller[name])

            elif robot.RobotMap.ControlMap.Controller[name]['jobType'] == 'side':
                SideCon[name] = robot.Creator.createControllers(robot.RobotMap.ControlMap.Controller[name])

        self.MainCon = MainCon
        self.SideCon = SideCon

        # button commands
        self.alignBtn = JoystickButton(self.getMainController(), 1)
        self.armUp = JoystickButton(self.getMainController(), 2)

        self.alignBtn.whenPressed(align.Align(self.robot, 0.8))
        self.armUp.whenPressed(setarmpos.SetArmPos(self.robot, 0.5, 6000))

    def getMainController(self):
        return self.MainCon['xbox']

    def getSideController(self):
        return self.SideCon['board']
