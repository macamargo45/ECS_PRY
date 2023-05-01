import random
import pygame
import esper
from src.ecs.components.c_charge_shield import CChargeShield

from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState
from src.ecs.components.tags.c_tag_shield import CTagShield
from src.engine.service_locator import ServiceLocator


def create_square(world: esper.World, size: pygame.Vector2,
                  pos: pygame.Vector2, vel: pygame.Vector2, col: pygame.Color) -> int:
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity,
                        CSurface(size, col))
    world.add_component(cuad_entity,
                        CTransform(pos))
    world.add_component(cuad_entity,
                        CVelocity(vel))
    return cuad_entity


def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity,
                        CTransform(pos))
    world.add_component(sprite_entity,
                        CVelocity(vel))
    world.add_component(sprite_entity,
                        CSurface.from_surface(surface))
    return sprite_entity


def create_enemy_square(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
    vel_max = enemy_info["velocity_max"]
    vel_min = enemy_info["velocity_min"]
    vel_range = random.randrange(vel_min, vel_max)
    velocity = pygame.Vector2(random.choice([-vel_range, vel_range]),
                              random.choice([-vel_range, vel_range]))
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity, CTagEnemy("Bouncer"))
    ServiceLocator.sounds_service.play(enemy_info["sound"])


def create_enemy_hunter(world: esper.World, pos: pygame.Vector2, enemy_info: dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
    velocity = pygame.Vector2(0, 0)
    enemy_entity = create_sprite(world, pos, velocity, enemy_surface)
    world.add_component(enemy_entity, CEnemyHunterState(pos))
    world.add_component(enemy_entity,
                        CAnimation(enemy_info["animations"]))
    world.add_component(enemy_entity, CTagEnemy("Hunter"))


def create_player_square(world: esper.World, player_info: dict, player_lvl_info: dict) -> int:
    player_sprite = ServiceLocator.images_service.get(player_info["image"])
    size = player_sprite.get_size()
    size = (size[0] / player_info["animations"]["number_frames"], size[1])
    pos = pygame.Vector2(player_lvl_info["position"]["x"] - (size[0] / 2),
                         player_lvl_info["position"]["y"] - (size[1] / 2))
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(world, pos, vel, player_sprite)
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity,
                        CAnimation(player_info["animations"]))
    world.add_component(player_entity, CPlayerState())
    return player_entity


def create_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity,
                        CEnemySpawner(level_data["enemy_spawn_events"]))


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()

    world.add_component(input_left,
                        CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right,
                        CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_up,
                        CInputCommand("PLAYER_UP", pygame.K_UP))
    world.add_component(input_down,
                        CInputCommand("PLAYER_DOWN", pygame.K_DOWN))

    pause_game = world.create_entity()
    world.add_component(pause_game,
                        CInputCommand("PAUSE_GAME", pygame.K_p))

    input_fire = world.create_entity()
    world.add_component(input_fire,
                        CInputCommand("PLAYER_FIRE", pygame.BUTTON_LEFT))
    
    input_active_shield = world.create_entity()
    world.add_component(input_active_shield,
                        CInputCommand("PLAYER_ACTIVE_SHIELD", pygame.BUTTON_RIGHT))


def create_bullet(world: esper.World,
                  mouse_pos: pygame.Vector2,
                  player_pos: pygame.Vector2,
                  player_size: pygame.Vector2,
                  bullet_info: dict):
    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
    bullet_size = bullet_surface.get_rect().size
    pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (bullet_size[0] / 2),
                         player_pos.y + (player_size[1] / 2) - (bullet_size[1] / 2))
    vel = (mouse_pos - player_pos)
    vel = vel.normalize() * bullet_info["velocity"]

    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())
    ServiceLocator.sounds_service.play(bullet_info["sound"])


def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_info: dict):
    explosion_surface = ServiceLocator.images_service.get(
        explosion_info["image"])
    vel = pygame.Vector2(0, 0)

    explosion_entity = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity,
                        CAnimation(explosion_info["animations"]))
    ServiceLocator.sounds_service.play(explosion_info["sound"])
    return explosion_entity


def create_interface(world: esper.World, interface_info: dict):
    text = interface_info["title"]["text"]
    font = ServiceLocator.texts_service.get(interface_info["title"]["font"],
                                            interface_info["title"]["size"])
    color = pygame.Color(interface_info["title"]["color"]["r"],
                         interface_info["title"]["color"]["g"],
                         interface_info["title"]["color"]["b"])
    pos = pygame.Vector2(interface_info["title"]["position"]["x"],
                         interface_info["title"]["position"]["y"])
    create_text(world, text, font, color, pos)

    text_desc = interface_info["description"]["text"]
    font_desc = ServiceLocator.texts_service.get(interface_info["description"]["font"],
                                                 interface_info["description"]["size"])
    color_desc = pygame.Color(interface_info["description"]["color"]["r"],
                              interface_info["description"]["color"]["g"],
                              interface_info["description"]["color"]["b"])
    pos_desc = pygame.Vector2(interface_info["description"]["position"]["x"],
                              interface_info["description"]["position"]["y"])
    create_text(world, text_desc, font_desc, color_desc, pos_desc)


def create_text(world: esper.World, text: str, font: pygame.font.Font, color: pygame.Color, pos: pygame.Vector2):
    text_entity = world.create_entity()
    world.add_component(text_entity,
                        CTransform(pos))
    world.add_component(text_entity,
                        CSurface.from_text(text, font, color))
    return text_entity


def create_pause_text(world: esper.World, interface_info: dict):
    font = ServiceLocator.texts_service.get(interface_info["pauseText"]["font"],
                                            interface_info["pauseText"]["size"])
    color = pygame.Color(interface_info["pauseText"]["color"]["r"],
                         interface_info["pauseText"]["color"]["g"],
                         interface_info["pauseText"]["color"]["b"])
    text = interface_info["pauseText"]["text"]
    pos = pygame.Vector2(280, 180)
    txt_ent = create_text(
        world, text, font, color, pos)
    return txt_ent


def create_special_shield_interface(world: esper.World, interface_info: dict, player_info: dict) -> int:
    text_desc_special = interface_info["shield"]["text"]
    font_desc_special = ServiceLocator.texts_service.get(interface_info["shield"]["font"],
                                                         interface_info["shield"]["size"])
    color_desc_special = pygame.Color(interface_info["shield"]["color"]["r"],
                                      interface_info["shield"]["color"]["g"],
                                      interface_info["shield"]["color"]["b"])
    pos_desc_special = pygame.Vector2(interface_info["shield"]["position"]["x"],
                                      interface_info["shield"]["position"]["y"])
    create_text(world, text_desc_special, font_desc_special,
                color_desc_special, pos_desc_special)

    charge_special_font = ServiceLocator.texts_service.get(
        interface_info["shieldPercentage"]["font"], interface_info["shieldPercentage"]["size"])
    charge_special_color = pygame.Color(0, 255, 0)
    charge_special_pos = pos_desc_special.copy() + pygame.Vector2(0, 15)
    charge_special_text = "100%"
    bullet_charge_text = create_text(
        world, charge_special_text, charge_special_font, charge_special_color, charge_special_pos)
    world.add_component(bullet_charge_text,
                        CChargeShield(player_info["charge_time_special"]))
    return bullet_charge_text

def create_shield(world: esper.World, playerPos: pygame.Vector2, player_info: dict) -> int:
    shield_surface = ServiceLocator.images_service.get(player_info["image_special"])
    shield_entity = create_sprite(world, playerPos, pygame.Vector2(0, 0), shield_surface)
    world.add_component(shield_entity, CTagShield())
    world.add_component(shield_entity, CAnimation(player_info["shield_animations"]))
