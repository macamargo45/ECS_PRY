import esper
from src.ecs.components.c_enemy_fly import CEnemyFly
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def get_and_change_army_direction(world: esper.World, change_direction=False) -> int:
    components = world.get_component(CEnemyFly)
    for _, c_sqd in components:
        if change_direction:
            c_sqd.dir *= -1
        return c_sqd.dir, c_sqd.dir_vel
    return 1, 1

def update_enemy_positions(world: esper.World, dir, vel, delta_time):
    components = world.get_components(CEnemyState, CTagEnemy)
    for _, (c_st, _) in components:
        c_st.move_pos.x += dir * vel * delta_time

def system_enemy_movement(world: esper.World, delta_time: float):
    left_most_x = None
    left_most_x_tr = None
    right_most_x = None
    right_most_x_tr = None
    components = world.get_components(CEnemyState, CTagEnemy, CTransform)
    for _, (c_st, _, c_t) in components:
        if left_most_x is None or c_st.move_pos.x < left_most_x:
            left_most_x = c_st.move_pos.x
            left_most_x_tr = c_t
        if right_most_x is None or c_st.move_pos.x > right_most_x:
            right_most_x = c_st.move_pos.x
            right_most_x_tr = c_t

    if left_most_x is None and right_most_x is None:
        dir, vel = get_and_change_army_direction(world)
    else:
        dir, vel = get_and_change_army_direction(world, left_most_x < 13 or right_most_x > 218)
        if left_most_x < 13:
            left_most_x_tr.pos.x = 13
        elif right_most_x > 218:
            right_most_x_tr.pos.x = 218

    update_enemy_positions(world, dir, vel, delta_time)
