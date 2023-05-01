import pygame
import esper
from src.ecs.components.c_charge_shield import CChargeShield
from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator


def system_charge_shield(world: esper.World, delta_time: float, interface_info: dict):
    components = world.get_components(CChargeShield, CSurface)
    for _, (c_c, c_s) in components:
        if not c_c.charged:
            color = pygame.Color(255, 0, 0)
            c_c.curr_charge_time += delta_time
            if c_c.curr_charge_time > c_c.charge_time:
                c_c.curr_charge_time = c_c.charge_time
                c_c.charged = True
        else:
            color = pygame.Color(0, 255, 0)
        font = ServiceLocator.texts_service.get(interface_info["shieldPercentage"]["font"],
                                                interface_info["shieldPercentage"]["size"])
        text = str(round((c_c.curr_charge_time / c_c.charge_time) * 100)) + "%"
        c_s.surf = font.render(text, True, color)
        c_s.area = c_s.surf.get_rect()
