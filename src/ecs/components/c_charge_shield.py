class CChargeShield():
    def __init__(self, charge_time) -> None:
        self.charge_time = charge_time
        self.curr_charge_time = charge_time
        self.charged = True