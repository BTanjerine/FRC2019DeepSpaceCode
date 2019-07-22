from wpilib.command import Command


class TeleOp(Command):
    def __init__(self, robot):
        super().__init__()
        self.robot = robot  # access robot values

        self.controller = robot.OI.getMainController()  # get controller class
        self.sideCon = robot.OI.getSideController()     # get side controller class
        self.shiftToggle = False    # drive gear shift toggle
        self.robot.lime.setLED(1)   # set limelight vals
        self.robot.lime.setCAM(1)

    def execute(self):
        y = -self.controller.getY(self.controller.Hand.kLeft)      # drive y axis percent output
        x = self.controller.getX(self.controller.Hand.kRight)       # drive x axis percent output
        # y = -self.sideCon.getY()
        # x = self.sideCon.getX()
        armUp = self.controller.getTriggerAxis(self.controller.Hand.kRight)     # arm up percent output
        armDown = self.controller.getTriggerAxis(self.controller.Hand.kLeft)    # arm down percent output

        # set drive percent to 0 if between 15% to -15%
        if -0.15 < abs(y) < 0.15:
            y = 0
        if -0.15 < abs(x) < 0.15:
            x = 0

        rgt = y - x  # calculate drive side powers
        lft = y + x

        self.robot.drive.set(rgt * 0.95, lft * 0.95)  # set power to drive

        # raise or lower arm when press trigger
        if armUp > 0:
            self.robot.arm.set(armUp*0.7)
        elif armDown > 0 and self.robot.arm.getZeroPos() == 1:
            self.robot.arm.set(-armDown*0.7)
        else:
            self.robot.arm.set(0)

        if not self.robot.arm.getZeroPos():
            self.robot.arm.resetHeight()

        # intake or outtake ball when press bumpers
        if self.controller.getBumper(self.controller.Hand.kRight):
            self.robot.intake.setIntake(0.95)
        elif self.controller.getBumper(self.controller.Hand.kLeft):
            self.robot.intake.setIntake(-0.95)
        else:
            self.robot.intake.setIntake(0)

        # shift drive gears when press right stick button
        if self.controller.getStickButton(self.controller.Hand.kRight) == True and self.shiftToggle == False:
            while self.controller.getStickButton(self.controller.Hand.kRight):
                pass
            self.robot.drive.ShiftGear(self.robot.drive.KtorqueMode)
            self.shiftToggle = True

        elif self.controller.getStickButton(self.controller.Hand.kRight) == True and self.shiftToggle == True:
            while self.controller.getStickButton(self.controller.Hand.kRight):
                pass
            self.robot.drive.ShiftGear(self.robot.drive.KspeedMode)
            self.shiftToggle = False

