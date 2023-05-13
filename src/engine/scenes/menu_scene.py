from src.ecs.systems.s_up_scroll import system_up_scroll
from src.ecs.components.c_up_scroll import CUpScroll
from src.ecs.components.c_blink import CBlink
from src.create.prefab_creator import create_banner
from src.create.prefab_creator import create_sprite
from src.engine.service_locator import ServiceLocator
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_animation import system_animation
from src.create.prefab_creator import create_starfield
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.systems.s_star_movement import system_star_movement
import pygame
from src.create.prefab_creator import create_text, TextAlignment
from src.engine.scenes.base_scene import Scene
from src.ecs.systems.s_blink import system_blink

class MenuScene(Scene):
    def do_create(self):
        create_starfield(self.ecs_world, self._game_engine.starfield_cfg, self.screen_rect)
        scroll_vel = self._game_engine.interface_cfg["menu_scroll_vel"]
        oneup_title = self._game_engine.interface_cfg["1up_title"]
        oneup_entity = create_text(self.ecs_world, oneup_title["text"], oneup_title["size"], 
                   pygame.Color(oneup_title["color"]["r"], oneup_title["color"]["g"], oneup_title["color"]["b"]), 
                   pygame.Vector2(oneup_title["position"]["x"], oneup_title["position"]["y"]), getattr(TextAlignment, oneup_title["alignment"]))
        self.ecs_world.add_component(oneup_entity, CUpScroll(oneup_title["position"]["y"],self.screen_rect.h, scroll_vel))

        hiscore_title = self._game_engine.interface_cfg["hi-score"]
        hiscore_entity = create_text(self.ecs_world, hiscore_title["text"], hiscore_title["size"], 
                   pygame.Color(hiscore_title["color"]["r"], hiscore_title["color"]["g"], hiscore_title["color"]["b"]), 
                   pygame.Vector2(hiscore_title["position"]["x"], hiscore_title["position"]["y"]), getattr(TextAlignment, hiscore_title["alignment"]))
        self.ecs_world.add_component(hiscore_entity, CUpScroll(hiscore_title["position"]["y"],self.screen_rect.h, scroll_vel))

        score_title = self._game_engine.interface_cfg["score"]
        score_entity = create_text(self.ecs_world, score_title["text"], score_title["size"], 
                   pygame.Color(score_title["color"]["r"], score_title["color"]["g"], score_title["color"]["b"]), 
                   pygame.Vector2(score_title["position"]["x"], score_title["position"]["y"]), getattr(TextAlignment, score_title["alignment"]))
        self.ecs_world.add_component(score_entity, CUpScroll(score_title["position"]["y"],self.screen_rect.h, scroll_vel))

        highestscore_title = self._game_engine.interface_cfg["highest-score"]
        highestscore_entity = create_text(self.ecs_world, highestscore_title["text"], highestscore_title["size"], 
                   pygame.Color(highestscore_title["color"]["r"], highestscore_title["color"]["g"], highestscore_title["color"]["b"]), 
                   pygame.Vector2(highestscore_title["position"]["x"], highestscore_title["position"]["y"]), getattr(TextAlignment, highestscore_title["alignment"]))
        self.ecs_world.add_component(highestscore_entity, CUpScroll(highestscore_title["position"]["y"],self.screen_rect.h, scroll_vel))
        
        banner_config = self._game_engine.interface_cfg["banner"]
        banner_surface = ServiceLocator.images_service.get(banner_config["image"])
        banner_entity = create_banner(self.ecs_world, 
                                      pygame.Vector2(banner_config["position"]["x"],banner_config["position"]["y"]), 
                                      banner_surface)
        self.ecs_world.add_component(banner_entity, CUpScroll(banner_config["position"]["y"],self.screen_rect.h, scroll_vel))


        pressstart_title = self._game_engine.interface_cfg["press-start"]
        pressstart_entity = create_text(self.ecs_world, pressstart_title["text"], pressstart_title["size"], 
                   pygame.Color(pressstart_title["color"]["r"], pressstart_title["color"]["g"], pressstart_title["color"]["b"]), 
                   pygame.Vector2(pressstart_title["position"]["x"], pressstart_title["position"]["y"]), getattr(TextAlignment, pressstart_title["alignment"]))
        self.ecs_world.add_component(pressstart_entity, CBlink(pressstart_title["blink_rate"]))
        self.ecs_world.add_component(pressstart_entity, CUpScroll(pressstart_title["position"]["y"],self.screen_rect.h, scroll_vel))


        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))
        

    def do_update(self, delta_time: float):
        system_up_scroll(self.ecs_world, delta_time)
        system_star_movement(self.ecs_world, delta_time, self.screen_rect.h)
        system_blink(self.ecs_world, delta_time)
        system_movement(self.ecs_world, delta_time)

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("LEVEL_01")