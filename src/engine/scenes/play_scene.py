import json
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_star_movement import system_star_movement
from src.create.prefab_creator import create_input_player, create_starfield
from src.create.prefab_creator_play import create_player
from src.engine.scenes.base_scene import Scene

class PlayScene(Scene):
    
    def do_create(self):
        create_starfield(self.ecs_world, self._game_engine.starfield_cfg, self.screen_rect)
        self.pl_entity, self.pl_tr, self.pl_v, self.pl_tg, self.pl_st = create_player(self.ecs_world)
        create_input_player(self.ecs_world)

    def do_update(self, delta_time: float):
        system_star_movement(self.ecs_world, delta_time, self.screen_rect.h)
        system_blink(self.ecs_world, delta_time)
        system_movement(self.ecs_world, delta_time)
        system_screen_player(self.ecs_world,self.screen_rect)


    def do_action(self, action: CInputCommand) -> None:
        if action.name == "PLAYER_LEFT":
            if action.phase == CommandPhase.START:
                self.pl_v.vel.x -= self.pl_tg.input_speed
            else:
                self.pl_v.vel.x += self.pl_tg.input_speed
        if action.name == "PLAYER_RIGHT":
            if action.phase == CommandPhase.START:
                self.pl_v.vel.x += self.pl_tg.input_speed
            else:
                self.pl_v.vel.x -= self.pl_tg.input_speed                 
            