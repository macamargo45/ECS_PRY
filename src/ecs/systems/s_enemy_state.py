import esper
import math
from src.create.prefab_creator_play import create_enemy_bullet

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_state import CEnemyState, EnemyStates
from src.ecs.components.c_manager_level import CManagerLevel
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_player_state import CPlayerState, PlayerState


def system_enemy_state(world: esper.World, lvl_mgr: CManagerLevel, player_tr: CTransform, player_st: CPlayerState, delta_time: float):

    components = world.get_components(
        CEnemyState, CVelocity, CSurface, CTransform, CAnimation)
    for _, (c_st, c_v, c_s, c_tr, c_a) in components:
        _calculate_bullet_generation(world, c_st, c_tr, player_tr, player_st)


def _calculate_bullet_generation(world: esper.World, c_st: CEnemyState, c_tr: CTransform, player_tr: CTransform, player_st: CPlayerState):
    if player_st.state == PlayerState.DEAD:
        return

    rnd = c_st.rng.randint(0, 2000)
    max_rdn = c_st.prob_fire
    if c_st.state == EnemyStates.ATTACK:
        max_rdn = c_st.prob_fire_attack
    if rnd > max_rdn:
        pos = c_tr.pos.copy()
        pos.x += 5
        pos.y += 5
        vel_x = 0
        if c_st.state == EnemyStates.ATTACK:
            vel_x = abs(player_tr.pos.x - pos.x)
            vel_x = min(5, vel_x)
            vel_x *= math.copysign(vel_x, player_tr.pos.x - pos.x)
        create_enemy_bullet(world, pos, vel_x)
