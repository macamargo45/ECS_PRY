import pygame
import esper
from typing import Tuple

from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator
from src.create.prefab_creator import create_text, TextAlignment


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
