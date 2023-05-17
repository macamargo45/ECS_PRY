from enum import Enum
import pygame 


class CBulletState:
    def __init__(self, velocity:pygame.Vector2) -> None:
        self.velocity = velocity
        self.state:BulletStates = BulletStates.IDLE

class BulletStates(Enum):
    IDLE = 0
    FIRED = 1
