import asyncio
import json
from src.engine.scenes.base_scene import Scene
from src.engine.scenes.gameove_scene import GameoverScene
from src.engine.scenes.menu_scene import MenuScene
from src.engine.scenes.play_scene import PlayScene
from src.engine.scenes.win_scene import WinScene
import pygame
import esper
from src.ecs.systems.s_animation import system_animation

from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet

from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_screen_bullet import system_screen_bullet

from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_enemy_hunter_state import system_enemy_hunter_state

from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet

from src.ecs.components.c_input_command import CInputCommand, CommandPhase

from src.create.prefab_creator import create_enemy_spawner, create_input_player, create_player_square, create_bullet, create_pause_text, create_interface


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]),
            pygame.SCALED)

        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_cfg["framerate"]
        self._delta_time = 0
        self._bg_color = pygame.Color(self.window_cfg["bg_color"]["r"],
                                     self.window_cfg["bg_color"]["g"],
                                     self.window_cfg["bg_color"]["b"])
        self.ecs_world = esper.World()

        self.num_bullets = 0

        self.paused = False
        
        self._scenes:dict[str, Scene] = {}
        self._scenes["MENU_SCENE"] = MenuScene(self)
        self._scenes["LEVEL_01"] = PlayScene(self)
        self._scenes["WIN_SCENE"] = WinScene(self)
        self._scenes["GAME_OVER_SCENE"] = GameoverScene(self)
        self._current_scene:Scene = None
        self._scene_name_to_switch:str = None

    def _load_config_files(self):
        with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("assets/cfg/enemies.json") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/level_01.json") as level_01_file:
            self.level_01_cfg = json.load(level_01_file)
        with open("assets/cfg/player.json") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/bullet.json") as bullet_file:
            self.bullet_cfg = json.load(bullet_file)
        with open("assets/cfg/explosion.json") as explosion_file:
            self.explosion_cfg = json.load(explosion_file)
        with open("assets/cfg/interface.json") as interface_file:
            self.interface_cfg = json.load(interface_file)
        with open("assets/cfg/starfield.json") as starfield_file:
            self.starfield_cfg = json.load(starfield_file)

    async def run(self, start_scene_name:str) -> None:
        self.is_running = True
        self._current_scene = self._scenes[start_scene_name]
        self._create()
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
            await asyncio.sleep(0)
        self._clean()
    
    def switch_scene(self, new_scene_name:str):
        self._scene_name_to_switch = new_scene_name

    def _create(self):
        self._current_scene.do_create()

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self._delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            self._current_scene.do_process_events(event)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self._current_scene.simulate(self._delta_time)

    def _draw(self):
        self.screen.fill(self._bg_color)        
        self._current_scene.do_draw(self.screen)
        pygame.display.flip()

    def _handle_switch_scene(self):
        if self._scene_name_to_switch is not None:
            self._current_scene.clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None

    def _do_action(self, action:CInputCommand):        
        self._current_scene.do_action(action)

    def _do_clean(self):
        if self._current_scene is not None:
            self._current_scene.clean()
        pygame.quit()