
import esper
from src.ecs.components.c_up_scroll import CUpScroll
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_up_scroll(world:esper.World, delta_time:float):
    components = world.get_components(CTransform, CUpScroll)

    c_t:CTransform
    c_us:CUpScroll
    for _, (c_t, c_us) in components:
        if c_us.pos_y > c_us.initial_position:
            c_us.pos_y -= (c_us.vel * delta_time) 
            c_t.pos.y = c_us.pos_y
