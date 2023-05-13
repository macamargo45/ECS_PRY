import pygame

class CBlink:
    def __init__(self, blink_rate:float) -> None:
        self.blink_rate = blink_rate
        self.curr_anim_time = blink_rate