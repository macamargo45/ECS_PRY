from enum import Enum
import random
import pygame
import esper

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
from src.ecs.components.c_blink import CBlink
from src.ecs.components.tags.c_tag_star import CTagStar
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


def create_banner(world: esper.World, pos: pygame.Vector2, surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity,
                        CTransform(pos))
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

    world.add_component(input_left, CInputCommand(
        "PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right, CInputCommand(
        "PLAYER_RIGHT", pygame.K_RIGHT))

    pause_game = world.create_entity()
    world.add_component(pause_game, CInputCommand("PAUSE_GAME", pygame.K_p))

    input_fire = world.create_entity()
    world.add_component(input_fire, CInputCommand("PLAYER_FIRE", pygame.K_z))


def create_bullet(world: esper.World, mouse_pos: pygame.Vector2, player_pos: pygame.Vector2, player_size: pygame.Vector2, bullet_info: dict):
    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
    bullet_size = bullet_surface.get_rect().size
    pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (
        bullet_size[0] / 2), player_pos.y + (player_size[1] / 2) - (bullet_size[1] / 2))
    vel = (mouse_pos - player_pos)
    vel = vel.normalize() * bullet_info["velocity"]

    bullet_entity = create_sprite(world, pos, vel, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())
    ServiceLocator.sounds_service.play(bullet_info["sound"])


def create_explosion(world: esper.World, pos: pygame.Vector2):
    explosion_info = ServiceLocator.configs_service.get("assets/cfg/explosion.json")
    explosion_surface = ServiceLocator.images_service.get(explosion_info["image"])
    vel = pygame.Vector2(0, 0)

    explosion_entity = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity,CAnimation(explosion_info["animations"]))
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


class TextAlignment(Enum):
    LEFT = 0,
    RIGHT = 1
    CENTER = 2


def create_text(world: esper.World, txt: str, size: int,
                color: pygame.Color, pos: pygame.Vector2, alignment: TextAlignment) -> int:
    font = ServiceLocator.fonts_service.get(
        "assets/fnt/PressStart2P.ttf", size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(txt, font, color))
    txt_s = world.component_for_entity(text_entity, CSurface)

    # De acuerdo al alineamiento, determia el origine de la superficie
    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= txt_s.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= txt_s.area.centerx

    world.add_component(text_entity,
                        CTransform(pos + origin))
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


def create_starfield(world: esper.World,
                     starfield_info: dict,
                     window_size: pygame.Rect):
    window_width = window_size.w
    window_height = window_size.h
    size = pygame.Vector2(1, 1)
    for starindex in range(starfield_info["number_of_stars"]):
        star_entity = world.create_entity()
        color_index = random.randint(0, len(starfield_info["star_colors"]) - 1)
        color = pygame.Color(
            starfield_info["star_colors"][color_index]["r"],
            starfield_info["star_colors"][color_index]["g"],
            starfield_info["star_colors"][color_index]["b"])
        vertical_speed = random.randint(
            starfield_info["vertical_speed"]["min"], starfield_info["vertical_speed"]["max"])
        blink_rate = random.uniform(
            starfield_info["blink_rate"]["min"], starfield_info["blink_rate"]["max"])
        initial_position = pygame.Vector2(random.randint(0, window_width),
                                          random.randint(0, window_height))
        world.add_component(star_entity, CSurface(size, color))
        world.add_component(star_entity, CTransform(initial_position))
        world.add_component(star_entity, CVelocity(
            pygame.Vector2(0, vertical_speed)))
        world.add_component(star_entity, CBlink(blink_rate))
        world.add_component(star_entity, CTagStar())
