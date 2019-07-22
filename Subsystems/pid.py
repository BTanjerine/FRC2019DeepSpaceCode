from wpilib.command import Subsystem


class PID(Subsystem):
    def __init__(self, kp, ki, kd):
        super().__init__()
        """
        kp -> constant value for Proportional input
        ki -> constant value for Iterative input
        kd -> Determines constant value for Derivative input
        """
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd

        self.pastError = 0

        self.p = 0
        self.i = 0
        self.d = 0

        self.output = 0

    def getError(self, curVal, desVal):
        # get distance from current
        return desVal - curVal

    def getP(self, curVal, desVal):
        self.p = self.getError(curVal, desVal) * self.Kp
        return self.p

    def getI(self, curVal, desVal):
        self.i = (self.getError(curVal, desVal) + self.i) * self.Ki
        if self.getError(curVal, desVal) == 0:
            self.i = 0

        return self.i

    def getD(self, curVal, desVal):
        self.d = (self.getError(curVal, desVal) - self.pastError)*self.Kd
        self.pastError = self.getError(curVal, desVal)
        return self.d

    def getOutputVal(self, power, curVal, desVal):
        self.output = self.getP(curVal, desVal) + self.getI(curVal, desVal) + self.getD(curVal, desVal)

        if self.output > power:
            self.output = power
        elif self.output < -power:
            self.output = -power

        return self.output