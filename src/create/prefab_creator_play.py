import pygame
import esper
from src.create.prefab_creator import TextAlignment, create_sprite, create_square, create_text
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_bullet_in_ship import CBulletInShip
from src.ecs.components.c_bullet_state import CBulletState
from src.ecs.components.c_enemy_fly import CEnemyFly
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def create_player(world: esper.World):
    player_config = ServiceLocator.configs_service.get(
        "assets/cfg/player.json")
    surface = ServiceLocator.images_service.get(player_config["image"])
    pos = pygame.Vector2(
        player_config["spawn_point"]["x"], player_config["spawn_point"]["y"])
    vel = pygame.Vector2(0, 0)

    player_entity = create_sprite(world, pos, vel, surface)

    world.add_component(player_entity, CTagPlayer(
        player_config["input_speed"]))
    world.add_component(player_entity, CPlayerState(
        player_config["lives"], player_config["respawn_time"]))

    player_tr = world.component_for_entity(player_entity, CTransform)
    player_v = world.component_for_entity(player_entity, CVelocity)
    player_tag = world.component_for_entity(player_entity, CTagPlayer)
    player_state = world.component_for_entity(player_entity, CPlayerState)
    player_surface = world.component_for_entity(player_entity, CSurface)
    return (player_entity, player_tr, player_v, player_tag, player_surface)


def create_player_bullet(world: esper.World, player_pos: pygame.Vector2, player_size: pygame.Vector2, player_entity: int) -> CBulletState:

    bullet_info = ServiceLocator.configs_service.get("assets/cfg/bullet.json")

    bullet_size = pygame.Vector2(
        bullet_info["size"]["w"],  bullet_info["size"]["h"])
    pos = pygame.Vector2(player_pos.x + (player_size[0]*3), player_pos.y)
    vel = pygame.Vector2(0, 0)
    color = pygame.Color(
        bullet_info["color"]["r"], bullet_info["color"]["g"], bullet_info["color"]["b"])

    val_bullet = pygame.Vector2(
        bullet_info["velocity"]["x"], bullet_info["velocity"]["y"])

    bullet_entity = create_square(world, bullet_size, pos, vel, color)

    world.add_component(bullet_entity, CTransform(pygame.Vector2()))
    world.add_component(bullet_entity, CBulletInShip(player_entity))

    bullet_state = CBulletState(val_bullet)
    world.add_component(bullet_entity, bullet_state)
    return bullet_state


def create_enemy(world: esper.World, pos: pygame.Vector2, velocity: pygame.Vector2, score_value: float, score_value_attack: float, image_path: str, animations: dict):
    image = ServiceLocator.images_service.get(image_path)
    enemy_entity = create_sprite(world, pos, velocity, image)
    world.add_component(enemy_entity, CTagEnemy(score_value))
    world.add_component(enemy_entity, CAnimation(animations))
    enemy_state = CEnemyState()
    world.add_component(enemy_entity, enemy_state)
    enemy_state.move_pos = pos.copy()


def create_army(world: esper.World):
    enemies_cfg = ServiceLocator.configs_service.get("assets/cfg/enemies.json")
    level_cfg = ServiceLocator.configs_service.get("assets/cfg/level_01.json")
    space_ships = 15
    global_speed = pygame.Vector2(0, 0)
    fleet_entity = world.create_entity()
    world.add_component(fleet_entity,
                        CEnemyFly(1, level_cfg["enemy_speed"]["x"]))

    enemy_configs = [
        enemies_cfg["invaders_enemy_04"],
        enemies_cfg["invaders_enemy_03"],
        enemies_cfg["invaders_enemy_02"],
        enemies_cfg["invaders_enemy_01"]
    ]

    start_positions = [
        pygame.Vector2(80, 39),
        pygame.Vector2(63, 54),
        pygame.Vector2(44, 66),
        pygame.Vector2(28, 80)
    ]

    for i, config in enumerate(enemy_configs):
        score_value = config["score_value"]
        score_value_attack = config["score_value_attack"]
        image = config["image"]
        animations = config["animations"]
        start_pos = start_positions[i]

        if i == 3:
            rows = 3
            cols = 10
        elif i == 2:
            rows = 1
            cols = 8
        elif i == 1:
            rows = 1
            cols = 6
        else:
            rows = 1
            cols = 2

        for row in range(rows):
            for col in range(cols):
                pos = pygame.Vector2(start_pos.x + 18 * col,
                                     start_pos.y + space_ships * row)
                create_enemy(world, pos, global_speed, score_value,
                             score_value_attack, image, animations)


def create_ready_text(world: esper.World) -> int:
    interface_cfg = ServiceLocator.configs_service.get(
        "assets/cfg/interface.json")
    color = pygame.Color(interface_cfg["ready_text_color"]["r"],
                         interface_cfg["ready_text_color"]["g"], interface_cfg["ready_text_color"]["b"])
    pos = pygame.Vector2(120, 100)
    game_start = create_text(world, "READY", 8, color,
                             pos, TextAlignment.CENTER)
    return game_start
