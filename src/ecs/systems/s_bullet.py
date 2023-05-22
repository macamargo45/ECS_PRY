from src.ecs.components.c_player_state import PlayerState
from src.ecs.components.c_player_state import CPlayerState
import pygame
import esper
from src.ecs.components.c_bullet_in_ship import CBulletInShip

from src.ecs.components.c_bullet_state import BulletStates, CBulletState
#from src.ecs.components.c_follow_entity import CFollowEntity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator

def system_bullet(world:esper.World, player_entity:int, screen_rect:pygame.Rect):

    bullet_info =  ServiceLocator.configs_service.get("assets/cfg/bullet.json")
    components_bullet = world.get_components(CSurface, CTransform, CVelocity, CBulletState)
    player_state = world.component_for_entity(player_entity, CPlayerState)

    for bullet, (c_s, c_tr, c_v, c_b_st) in components_bullet:
        bullet_rect = c_s.area.copy()
        bullet_rect.topleft = c_tr.pos.copy()

        if c_b_st.state == BulletStates.FIRED:
            if player_state.state == PlayerState.MOVE:
                if c_v.vel.x == 0 and c_v.vel.y == 0:
                    ServiceLocator.sounds_service.play(bullet_info["sound"])

                if world.has_component(bullet, CBulletInShip):
                    world.remove_component(bullet, CBulletInShip)

                c_v.vel = c_b_st.velocity.copy()
                if not screen_rect.contains(bullet_rect):
                    c_b_st.state = BulletStates.IDLE
                
        elif c_b_st.state == BulletStates.IDLE:
            c_v.vel = pygame.Vector2(0, 0)
            world.add_component(bullet, CBulletInShip(player_entity))
