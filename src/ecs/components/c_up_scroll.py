import pygame

class CUpScroll:
    def __init__(self, initial_position:int, scroll_size:int, vel: int) -> None:
        self.initial_position = initial_position
        self.pos_y = initial_position + scroll_size
        self.vel = vel