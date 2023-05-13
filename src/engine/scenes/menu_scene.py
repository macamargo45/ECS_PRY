from src.ecs.systems.s_star_blink import system_star_blink
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_animation import system_animation
from src.create.prefab_creator import create_starfield
from src.ecs.components.c_input_command import CInputCommand
import pygame
from src.create.prefab_creator import create_text
from src.engine.scenes.base_scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.systems.s_star_blink import system_star_blink

class MenuScene(Scene):
    def do_create(self):
        create_starfield(self.ecs_world, self._game_engine.starfield_cfg, self.screen_rect)
        # create_text(self.ecs_world, "MAIN MENU", 16, 
        #            pygame.Color(50, 255, 50), pygame.Vector2(320, 150), TextAlignment.CENTER)
        #create_text(self.ecs_world, "PRESS Z TO START GAME", 11, 
        #            pygame.Color(255, 255, 0), pygame.Vector2(320, 210), TextAlignment.CENTER)
        #create_text(self.ecs_world, "Arrows to MOVE - P to PAUSE", 8, 
        #            pygame.Color(150, 150, 255), pygame.Vector2(320, 250), TextAlignment.CENTER)
        
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))
        

    def do_update(self, delta_time: float):
        system_movement(self.ecs_world, delta_time)
        system_star_blink(self.ecs_world, delta_time, self.screen_rect.h)

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("LEVEL_01")