import pygame
import esper
from src.ecs.components.c_surface import CSurface

from src.ecs.components.tags.c_tag_score import CTagScore
from src.ecs.components.tags.c_tag_update_text import CTagUpdateText
from src.engine.service_locator import ServiceLocator


def system_update_interface(world: esper.World):

    score_query = world.get_components(CTagScore, CTagUpdateText, CSurface)
    interface_cfg = ServiceLocator.configs_service.get(
        "assets/cfg/interface.json")
    high_score_color = pygame.color.Color(interface_cfg["high_score_color"]["r"],
                                          interface_cfg["high_score_color"]["g"],
                                          interface_cfg["high_score_color"]["b"])
    font = ServiceLocator.fonts_service.get("./assets/fnt/PressStart2P.ttf", 8)
    for _, (c_tag_scr, c_tag_up_txt, c_s) in score_query:
        new_score = f"{ServiceLocator.general_service.score:02d}"
        c_s.surf = font.render(new_score, True, high_score_color)
        c_s.area = c_s.surf.get_rect()
