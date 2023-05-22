

from typing import Callable
from src.engine.service_locator import ServiceLocator
from src.ecs.components.c_player_state import PlayerState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.tags.c_tag_enemybullet import CTagEnemyBullet
import esper
from src.ecs.components.c_bullet_state import BulletStates, CBulletState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.create.prefab_creator import create_explosion


def system_collision_player_enemybullet(world: esper.World, do_action: Callable[[CInputCommand], None]):
    player_components = world.get_components(CSurface, CTransform, CPlayerState)
    components_enemybullet = world.get_components(CSurface, CTransform, CTagEnemyBullet)

    for player,(p_s, p_t, p_st) in player_components:
        if p_st.state == PlayerState.MOVE:
            player_rect = p_s.area.copy()
            player_rect.topleft = p_t.pos
            for bullet_entity, (c_b_s, c_b_t, c_b_st) in components_enemybullet:
                bull_rect = c_b_s.area.copy()
                bull_rect.topleft = c_b_t.pos
                if player_rect.colliderect(bull_rect):
                    world.delete_entity(bullet_entity)
                    create_explosion(world, p_t.pos,"player")
                    ServiceLocator.sounds_service.play("assets/snd/player_die.ogg")

                    p_st.lives -= 1
                    if p_st.lives >= 0:
                        p_st.state = PlayerState.IDLE
                    else:
                        p_st.state = PlayerState.DEAD
                        c_input = CInputCommand("GAME_OVER",None)
                        do_action(c_input)

