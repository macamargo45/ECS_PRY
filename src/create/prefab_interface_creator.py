import pygame
import esper
from typing import Tuple

from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_score import CTagScore
from src.ecs.components.tags.c_tag_update_text import CTagUpdateText
from src.engine.service_locator import ServiceLocator
from src.create.prefab_creator import create_text, TextAlignment
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_vertical_card import CVerticalCard


def create_paused_text(world: esper.World) -> Tuple[CSurface, CBlink, int]:
    interface_cfg = ServiceLocator.configs_service.get(
        "assets/cfg/interface.json")
    color = pygame.Color(interface_cfg["pause_text_color"]["r"],
                         interface_cfg["pause_text_color"]["g"],
                         interface_cfg["pause_text_color"]["b"])
    pos = pygame.Vector2(120, 100)
    paused_com = create_text(world, "PAUSE", 8, color, pos,
                             TextAlignment.CENTER)

    paused_s = world.component_for_entity(paused_com, CSurface)
    paused_blk = CBlink(interface_cfg["interface_blink_rate"])
    world.add_component(paused_com, paused_blk)
    paused_s.visible = False
    paused_blk.enabled = False
    return paused_s, paused_blk, paused_com


def create_gameover_text(world: esper.World):
    interface_cfg = ServiceLocator.configs_service.get(
        "assets/cfg/interface.json")
    color = pygame.Color(interface_cfg["gameover_text_color"]["r"],
                         interface_cfg["gameover_text_color"]["g"],
                         interface_cfg["gameover_text_color"]["b"])
    pos = pygame.Vector2(120, 100)
    paused_com = create_text(world, "GAME OVER", 8, color, pos,
                             TextAlignment.CENTER)

    world.component_for_entity(paused_com, CSurface)


def create_menu(world: esper.World, use_v_card: bool) -> None:
    interface_cfg = ServiceLocator.configs_service.get(
        "assets/cfg/interface.json")
    vertical_card = interface_cfg["vertical_card"]
    title_text_color = pygame.color.Color(interface_cfg["title_text_color"]["r"],
                                          interface_cfg["title_text_color"]["g"],
                                          interface_cfg["title_text_color"]["b"])
    normal_text_color = pygame.color.Color(interface_cfg["base_text_color"]["r"],
                                           interface_cfg["base_text_color"]["g"],
                                           interface_cfg["base_text_color"]["b"])
    high_score_color = pygame.color.Color(interface_cfg["high_score_color"]["r"],
                                          interface_cfg["high_score_color"]["g"],
                                          interface_cfg["high_score_color"]["b"])

    player_score = f"{ServiceLocator.general_service.score:02d}"

    if ServiceLocator.general_service.high_score > int(interface_cfg["high_score_max_value"]):
        high_score_max_value = str(
            ServiceLocator.general_service.high_score)
    else:
        high_score_max_value = str(interface_cfg["high_score_max_value"])

    ServiceLocator.general_service.high_score = int(high_score_max_value)

    one_up_txt = create_text(world, "1UP", 8, title_text_color,
                             pygame.Vector2(32, 18), TextAlignment.LEFT)

    hiscore_text = create_text(world, "HI-SCORE", 8, title_text_color,
                               pygame.Vector2(90, 18), TextAlignment.LEFT)

    max_score_text = create_text(world, high_score_max_value, 8,
                                 high_score_color, pygame.Vector2(148, 28), TextAlignment.RIGHT)

    world.add_component(max_score_text, CTagScore(True))
    world.add_component(max_score_text, CTagUpdateText())

    score_value = create_text(world, player_score, 8, normal_text_color,
                              pygame.Vector2(72, 28), TextAlignment.RIGHT)
    world.add_component(score_value, CTagScore(False))

    if use_v_card:
        add_v_card_component(world, one_up_txt, 18,
                             vertical_card["v_speed"], vertical_card["v_offset"])
        add_v_card_component(world, hiscore_text, 18,
                             vertical_card["v_speed"], vertical_card["v_offset"])
        add_v_card_component(world, max_score_text, 28,
                             vertical_card["v_speed"], vertical_card["v_offset"])
        add_v_card_component(world, score_value, 28,
                             vertical_card["v_speed"], vertical_card["v_offset"])


def add_v_card_component(world: esper.World, entity: int, pos_y: float,
                         v_speed: float, v_offset: float):
    world.add_component(entity, CVelocity(pygame.Vector2(0, 0)))
    world.add_component(entity, CVerticalCard(
        v_speed, pos_y + v_offset, pos_y))
