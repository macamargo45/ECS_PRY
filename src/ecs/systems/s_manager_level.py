import esper

from src.ecs.components.c_manager_level import CManagerLevel, LevelState
from src.create.prefab_creator_play import create_army

def system_level_manager(world:esper.World, c_mng_lvl:CManagerLevel, delta_time:float):
    if c_mng_lvl.state == LevelState.START:
        c_mng_lvl.time_on_state += delta_time
        if c_mng_lvl.time_on_state > c_mng_lvl.time_to_start_max:
            create_army(world)
            world.delete_entity(c_mng_lvl.ready_text_entity)
            c_mng_lvl.state = LevelState.PLAY
        return
    elif c_mng_lvl.state == LevelState.PLAY:
        pass

    elif c_mng_lvl.state == LevelState.PAUSED:
        pass
            