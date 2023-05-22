import json
from src.ecs.systems.s_player_state import system_player_state
from src.create.prefab_interface_creator import create_gameover_text
from src.ecs.systems.s_collision_player_enemybullet import system_collision_player_enemybullet
from src.ecs.systems.s_enemy_bullet import system_enemy_bullet
from src.ecs.components.c_bullet_state import BulletStates
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_manager_level import CManagerLevel, LevelState
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_bullet import system_bullet
from src.ecs.systems.s_bullet_in_ship import system_bullet_in_ship
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet
from src.ecs.systems.s_explosion_kill import system_explosion_kill
from src.ecs.systems.s_manager_level import system_level_manager
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_start_movement import system_start_movement
from src.ecs.systems.s_enemy_movement import system_enemy_movement
from src.ecs.systems.s_enemy_state import system_enemy_state
from src.create.prefab_creator import create_input_player, create_starfield
from src.create.prefab_creator_play import create_army, create_player, create_player_bullet, create_ready_text
from src.create.prefab_interface_creator import create_paused_text, create_menu
from src.engine.scenes.base_scene import Scene
from src.engine.service_locator import ServiceLocator


class PlayScene(Scene):

    def do_create(self):

        create_starfield(
            self.ecs_world, self._game_engine.starfield_cfg, self.screen_rect)
        self.pl_entity, self.pl_tr, self.pl_v, self.pl_tg, self.pl_cs = create_player(
            self.ecs_world)
        self.bullet = create_player_bullet(
            self.ecs_world, self.pl_tr.pos, self.pl_cs.area.size, self.pl_entity)
        create_input_player(self.ecs_world)

        ready_text_ent = create_ready_text(self.ecs_world)

        c_level = self.ecs_world.create_entity()
        self.c_manager_level = CManagerLevel(ready_text_ent)
        self.ecs_world.add_component(c_level, self.c_manager_level)

        self.level_cfg = ServiceLocator.configs_service.get(
            "assets/cfg/level_01.json")
        
        ServiceLocator.sounds_service.play(self.level_cfg["ready_game_sound"])

        create_menu(self.ecs_world, False)

    def do_update(self, delta_time: float):
        system_start_movement(self.ecs_world, delta_time, self.screen_rect.h)
        if self.c_manager_level.state != LevelState.PAUSED:
            system_player_state(self.ecs_world, self._game_engine.player_cfg, delta_time)
            system_movement(self.ecs_world, delta_time)
            system_enemy_movement(self.ecs_world, delta_time)
            system_enemy_state(self.ecs_world)
            system_bullet(self.ecs_world, self.pl_entity, self.screen_rect)
            system_bullet_in_ship(self.ecs_world)
            system_collision_enemy_bullet(self.ecs_world)
            system_explosion_kill(self.ecs_world)
            system_enemy_bullet(self.ecs_world, self.pl_entity, self._game_engine.enemybullet_cfg)
            system_collision_player_enemybullet(self.ecs_world, self.do_action)
            system_animation(self.ecs_world, delta_time)


        system_blink(self.ecs_world, delta_time)
        system_screen_player(self.ecs_world, self.screen_rect)
        system_level_manager(self.ecs_world, self.c_manager_level, delta_time)

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

        if action.name == "PLAYER_FIRE" and action.phase == CommandPhase.START:
            self.bullet.state = BulletStates.FIRED

        if action.name == "PAUSE_GAME" and action.phase == CommandPhase.END:
            if self.c_manager_level.state == LevelState.PLAY:
                self.c_manager_level.state = LevelState.PAUSED
                self.paused_state, paused_blink, self.pause_com = create_paused_text(
                    self.ecs_world)
            elif self.c_manager_level.state == LevelState.PAUSED:
                self.c_manager_level.state = LevelState.PLAY
                self.ecs_world.delete_entity(self.pause_com)
            is_paused = self.c_manager_level.state == LevelState.PAUSED
            if is_paused:
                ServiceLocator.sounds_service.play(
                    self.level_cfg["pause_game_sound"])

        if action.name == "GAME_OVER":
            print("TERMINADO")
            create_gameover_text(self.ecs_world)
            ServiceLocator.sounds_service.play("assets/snd/game_over.ogg")

