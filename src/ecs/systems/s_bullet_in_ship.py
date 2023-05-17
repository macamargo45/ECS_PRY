import esper

from src.ecs.components.c_bullet_in_ship import CBulletInShip
from src.ecs.components.c_transform import CTransform

def system_bullet_in_ship(world:esper.World):
    components = world.get_components(CTransform, CBulletInShip)

    for _, (c_t, c_b_s) in components:
        if not world.entity_exists(c_b_s.ship_follow):
            continue
        c_b_s_tr = world.try_component(c_b_s.ship_follow, CTransform)
        if c_b_s_tr is not None:
            c_t.pos.x = (c_b_s_tr.pos.x + 7) 
            c_t.pos.y = c_b_s_tr.pos.y 