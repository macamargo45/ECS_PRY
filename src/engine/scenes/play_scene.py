import json
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_star_movement import system_star_movement
from src.create.prefab_creator import create_starfield
from src.engine.scenes.base_scene import Scene

class PlayScene(Scene):
    def __init__(self, level_path:str, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        with open(level_path) as level_file:
            self.level_cfg = json.load(level_file)

    def do_create(self):
        create_starfield(self.ecs_world, self._game_engine.starfield_cfg, self.screen_rect)


    def do_update(self, delta_time: float):
        system_star_movement(self.ecs_world, delta_time, self.screen_rect.h)
        system_blink(self.ecs_world, delta_time)
        system_movement(self.ecs_world, delta_time)