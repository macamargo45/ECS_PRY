import esper

from src.ecs.components.tags.c_tag_star import CTagStar
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_transform import CTransform

def system_start_movement(world:esper.World, delta_time:float, window_height: int):
    components = world.get_components(CTransform, CTagStar)
    for _, (c_t, c_ts) in components:
        if c_t.pos.y > window_height:
            c_t.pos.y = 0
