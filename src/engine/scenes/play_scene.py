import json
from src.ecs.components.c_bullet_state import BulletStates
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_manager_level import CManagerLevel
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_bullet import system_bullet
from src.ecs.systems.s_bullet_in_ship import system_bullet_in_ship
from src.ecs.systems.s_collision_enemy_bullet import system_collision_enemy_bullet
from src.ecs.systems.s_manager_level import system_level_manager
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_star_movement import system_star_movement
from src.ecs.systems.s_enemy_movement import system_enemy_movement
from src.ecs.systems.s_enemy_state import system_enemy_state
from src.create.prefab_creator import create_input_player, create_starfield
from src.create.prefab_creator_play import create_army, create_player, create_player_bullet, create_ready_text
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

        c_lvl_st = self.ecs_world.create_entity()
        self.c_mng_lvl = CManagerLevel(ready_text_ent)
        self.ecs_world.add_component(c_lvl_st, self.c_mng_lvl)
        self.level_cfg = ServiceLocator.configs_service.get("assets/cfg/level_01.json")
        ServiceLocator.sounds_service.play(self.level_cfg["ready_game_sound"])

    def do_update(self, delta_time: float):
        system_star_movement(self.ecs_world, delta_time, self.screen_rect.h)
        system_blink(self.ecs_world, delta_time)
        system_movement(self.ecs_world, delta_time)
        system_screen_player(self.ecs_world, self.screen_rect)
        system_bullet(self.ecs_world, self.pl_entity, self.screen_rect)
        system_bullet_in_ship(self.ecs_world)
        system_animation(self.ecs_world, delta_time)
        system_collision_enemy_bullet(self.ecs_world)
        system_enemy_movement(self.ecs_world, delta_time)
        system_enemy_state(self.ecs_world)
        system_level_manager(self.ecs_world,self.c_mng_lvl,delta_time)

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

        if action.name == "PLAYER_FIRE":
            self.bullet.state = BulletStates.FIRED
