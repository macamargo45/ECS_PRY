import random
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator import create_bullet, create_enemybullet
import pygame
import esper
from src.ecs.components.c_bullet_in_ship import CBulletInShip
from src.ecs.components.c_enemy_fly import CEnemyFly

from src.ecs.components.c_bullet_state import BulletStates
#from src.ecs.components.c_follow_entity import CFollowEntity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator

def system_enemy_bullet(world:esper.World, player_entity:int, enemybullet_info:dict):

    p_s = world.component_for_entity(player_entity, CPlayerState)
    if p_s.state == PlayerState.MOVE:
        enemy_components = world.get_components(CSurface, CTransform, CTagEnemy)
        for enemy, (c_s, c_tr, c_ef) in enemy_components:
            fire_bullet = random.randint( 0, 1000)
            if fire_bullet < enemybullet_info["fire_cadence"]:
                create_enemybullet(world, c_tr.pos, c_s.area, enemybullet_info)