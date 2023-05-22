import pygame
import esper

from src.ecs.components.c_bullet_state import BulletStates, CBulletState
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator import create_explosion


def system_collision_enemy_bullet(world: esper.World):
    components_enemy = world.get_components(CSurface, CTransform, CTagEnemy)
    components_bullet = world.get_components(
        CSurface, CTransform, CBulletState)

    for enemy_entity, (c_s, c_t, c_ene) in components_enemy:
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        for bullet_entity, (c_b_s, c_b_t, c_b_st) in components_bullet:
            bull_rect = c_b_s.area.copy()
            bull_rect.topleft = c_b_t.pos
            if ene_rect.colliderect(bull_rect):
                world.delete_entity(enemy_entity)
                create_explosion(world, c_t.pos)
                c_b_st.state = BulletStates.IDLE
            _check_player_collision(world, bull_rect, c_b_st, bullet_entity)


def _check_player_collision(world: esper.World, bullet_rect: pygame.Rect,
                            c_b_st: CBulletState, b_ent: int):
    player_query = world.get_components(CPlayerState, CSurface, CTransform)
    for pl_ent, (c_pl_st, c_pl_s, c_pl_t) in player_query:
        player_rect = c_pl_s.area.copy()
        player_rect.topleft = c_pl_t.pos.copy()
        if bullet_rect.colliderect(player_rect) \
                and c_b_st.state == BulletStates.FIRED and c_b_st.type == "enemy" and c_pl_st.state == PlayerState.ALIVE:
            world.delete_entity(b_ent)
            player_killed(world, c_pl_st, c_pl_s, c_pl_t)


def player_killed(world: esper.World, c_st: CPlayerState, c_s: CSurface, c_t: CTransform):
    c_st.state = PlayerState.DEAD
    blast_pos = c_t.pos.copy() - pygame.Vector2(c_s.area.centerx, c_s.area.centery)

    bullet_component = world.get_components(CBulletState)
    for b_ent, c_b_st in bullet_component:
        if c_b_st.type == "player":
            world.delete_entity(b_ent)
    create_explosion(world, blast_pos, "player")
