import pygame
import esper
from src.create.prefab_creator import create_sprite
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def create_player(world: esper.World):
    player_config = ServiceLocator.configs_service.get("assets/cfg/player.json")
    surface = ServiceLocator.images_service.get(player_config["image"])
    pos = pygame.Vector2(player_config["spawn_point"]["x"], player_config["spawn_point"]["y"])
    vel = pygame.Vector2(0, 0)
    print(pos)
    player_entity = create_sprite(world, pos, vel, surface)

    world.add_component(player_entity, CTagPlayer(player_config["input_speed"]))
    world.add_component(player_entity, CPlayerState(player_config["lives"]))
    
    player_tr = world.component_for_entity(player_entity, CTransform)
    player_v = world.component_for_entity(player_entity, CVelocity)
    player_tag = world.component_for_entity(player_entity, CTagPlayer)
    player_state = world.component_for_entity(player_entity, CPlayerState)
    return (player_entity, player_tr, player_v, player_tag, player_state)