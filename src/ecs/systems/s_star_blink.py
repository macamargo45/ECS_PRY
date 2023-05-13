import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_star_blink import CStarBlink
from src.ecs.components.c_transform import CTransform

def system_star_blink(world:esper.World, delta_time:float, window_height: int):
    components = world.get_components(CSurface, CStarBlink, CTransform)
    for _, (c_s, c_sb, c_t) in components:
        # Dimsinuir el valor de curr_time de la animacion
        c_sb.curr_anim_time -= delta_time
        # Cuando curr_imte <= 0
        if c_sb.curr_anim_time <= 0:
            # RESTAURAR EL TIEMPO
            c_sb.curr_anim_time = c_sb.blink_rate
            c_s.visible = not c_s.visible
        if c_t.pos.y > window_height:
            c_t.pos.y = 0
