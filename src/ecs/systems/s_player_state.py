from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
import esper
import pygame

from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_velocity import CVelocity


def system_player_state(world: esper.World, player_cfg:dict, delta_time:float):
    components = world.get_components(CPlayerState, CSurface, CTransform)
    for _, (c_st, c_s, c_t) in components:
        if c_st.state == PlayerState.IDLE:
            _do_player_idle(c_st, c_s, c_t, player_cfg, delta_time)
        elif c_st.state == PlayerState.MOVE:
            _do_player_move(c_st)
        elif c_st.state == PlayerState.DEAD:
            _do_player_dead(c_s, c_t)


def _do_player_idle(c_st: CPlayerState, c_s:CSurface, c_t: CTransform, player_cfg:dict, delta_time:float):
    c_st.actual_respawn_time -= delta_time
    if c_st.actual_respawn_time <= 0:
        c_s.visible = True
        c_t.pos = pygame.Vector2(player_cfg["spawn_point"]["x"],player_cfg["spawn_point"]["y"])
        c_st.actual_respawn_time = c_st.respawn_time
        c_st.state = PlayerState.MOVE
    else:
        c_s.visible = False
        c_t.pos = pygame.Vector2(-1 * player_cfg["spawn_point"]["x"],player_cfg["spawn_point"]["y"])

    

def _do_player_move(c_st: CPlayerState):
    pass

def _do_player_dead(c_s: CSurface, c_t: CTransform,):
    c_s.visible = False
    c_t.pos = pygame.Vector2(-100, -100)
