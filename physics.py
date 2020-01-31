from pyfrc.physics import motor_cfgs, tankmodel
from pyfrc.physics.units import units

ENC_TICK_PER_FT = 229.1832


class PhysicsEngine(object):
    def __init__(self, physics_controller):
        super().__init__()
        self.physController = physics_controller
        self.bumperW = 3.25 * units.inch

        # 16.36
        self.Drive = tankmodel.TankModel.theory(
            motor_cfgs.MOTOR_CFG_MINI_CIM,
            115*units.lbs,
            16.36,
            3,
            11.12*units.inch,
            (28*units.inch + 2*self.bumperW),
            (31*units.inch + 2*self.bumperW),
            6*units.inch
        )

        self.lf_enc = 0
        self.rf_enc = 0

        self.gyro = 0

        self.roboAngle = 0

    def update_sim(self, hal_data, now, tm_dif):
        # simulate drive
        lf_motor = -hal_data['CAN'][9]['value']
        rf_motor = hal_data['CAN'][1]['value']

        self.lf_enc = self.Drive.l_position * ENC_TICK_PER_FT
        self.rf_enc = self.Drive.r_position * ENC_TICK_PER_FT

        hal_data['encoder'][0]['count'] = int(self.lf_enc)
        hal_data['encoder'][2]['count'] = int(self.rf_enc)

        x, y, angle = self.Drive.get_distance(lf_motor, rf_motor, tm_dif)
        self.physController.distance_drive(x, y, angle)
