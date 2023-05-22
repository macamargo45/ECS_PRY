from enum import Enum

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_blink import CBlink


class LevelState(Enum):
    START = 0
    PLAY = 1
    PAUSED = 2
    NEXT_LEVEL = 3
    GAME_OVER = 4


class CManagerLevel:
    def __init__(self, ready_text_entity: int):
        self.state: LevelState = LevelState.START

        self.time_on_state = 0
        self.time_to_next_level_max = 4

        self.time_to_start_max = 2.5

        self.start_text_ent = -1
        self.win_text_ent = -1
        self.win_text_ent_2 = -1

        self.ready_text_entity = ready_text_entity
