

import esper
from src.ecs.components.c_bullet_state import BulletStates, CBulletState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.create.prefab_creator import create_explosion
from src.engine.service_locator import ServiceLocator


def system_collision_enemy_bullet(world: esper.World):
    components_enemy = world.get_components(CSurface, CTransform, CTagEnemy)
    components_bullet = world.get_components(CSurface, CTransform, CBulletState)

    for enemy_entity, (c_s, c_t, c_ene_tag) in components_enemy:
        ene_rect = c_s.area.copy()
        ene_rect.topleft = c_t.pos
        for bullet_entity, (c_b_s, c_b_t, c_b_st) in components_bullet:
            bull_rect = c_b_s.area.copy()
            bull_rect.topleft = c_b_t.pos
            if ene_rect.colliderect(bull_rect):
                world.delete_entity(enemy_entity)
                ServiceLocator.general_service.score += c_ene_tag.score_value
                create_explosion(world, c_t.pos,"enemy")
                c_b_st.state = BulletStates.IDLE

