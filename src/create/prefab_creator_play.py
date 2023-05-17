import pygame
import esper
from src.create.prefab_creator import create_sprite, create_square
from src.ecs.components.c_bullet_in_ship import CBulletInShip
from src.ecs.components.c_bullet_state import CBulletState
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def create_player(world: esper.World):
    player_config = ServiceLocator.configs_service.get("assets/cfg/player.json")
    surface = ServiceLocator.images_service.get(player_config["image"])
    pos = pygame.Vector2(player_config["spawn_point"]["x"], player_config["spawn_point"]["y"])
    vel = pygame.Vector2(0, 0)

    player_entity = create_sprite(world, pos, vel, surface)

    world.add_component(player_entity, CTagPlayer(player_config["input_speed"]))
    world.add_component(player_entity, CPlayerState(player_config["lives"]))
    
    player_tr = world.component_for_entity(player_entity, CTransform)
    player_v = world.component_for_entity(player_entity, CVelocity)
    player_tag = world.component_for_entity(player_entity, CTagPlayer)
    player_state = world.component_for_entity(player_entity, CPlayerState)
    player_surface = world.component_for_entity(player_entity, CSurface)
    return (player_entity, player_tr, player_v, player_tag, player_surface)


def create_player_bullet(world: esper.World,player_pos: pygame.Vector2,player_size: pygame.Vector2,player_entity:int) ->CBulletState:
    
    bullet_info = ServiceLocator.configs_service.get("assets/cfg/bullet.json")

    bullet_size = pygame.Vector2(bullet_info["size"]["w"],  bullet_info["size"]["h"])
    pos = pygame.Vector2(player_pos.x + (player_size[0]*3),player_pos.y)
    vel = pygame.Vector2(0, 0)
    color = pygame.Color(bullet_info["color"]["r"], bullet_info["color"]["g"],bullet_info["color"]["b"])

    val_bullet = pygame.Vector2(bullet_info["velocity"]["x"], bullet_info["velocity"]["y"])

    bullet_entity = create_square(world, bullet_size, pos, vel, color)

    world.add_component(bullet_entity, CTransform(pygame.Vector2()))
    world.add_component(bullet_entity, CBulletInShip(player_entity))

    bullet_state = CBulletState(val_bullet)
    world.add_component(bullet_entity,bullet_state )
    return bullet_state