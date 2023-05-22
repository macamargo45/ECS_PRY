from enum import Enum
import pygame 


class CBulletState:
    def __init__(self, velocity:pygame.Vector2, type:str) -> None:
        self.velocity = velocity
        self.state:BulletStates = BulletStates.IDLE
        self.type = type

class BulletStates(Enum):
    IDLE = 0
    FIRED = 1
