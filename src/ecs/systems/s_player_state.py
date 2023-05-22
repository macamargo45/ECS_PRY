import esper

from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_manager_level import CManagerLevel, LevelState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator
from src.create.prefab_creator_interface import create_game_over_text
from src.create.prefab_creator_play import create_player_bullet


def system_player_state(world: esper.World, c_lvl_mgr: CManagerLevel, delta_time: float):
    player_cfg = ServiceLocator.configs_service.get("assets/cfg/player.json")
    components = world.get_components(CPlayerState, CSurface, CTransform)
    for pl_ent, (c_st, c_s, c_tr) in components:
        if c_st.state == PlayerState.ALIVE:
            pass
        elif c_st.state == PlayerState.DEAD:
            c_s.visible = False
            c_st.curr_dead_time += delta_time
            if c_st.curr_dead_time >= c_st.max_deaths:
                if c_st.lives > 0:
                    c_st.lives -= 1
                    c_tr.pos.x = player_cfg["spawn_point"]["x"]
                    c_tr.pos.y = player_cfg["spawn_point"]["y"]
                    c_st.curr_dead_time = 0
                    c_s.visible = True
                    c_st.state = PlayerState.ALIVE
                    c_lvl_mgr.bullet_state = create_player_bullet(world, pl_ent)
                else:
                    if c_lvl_mgr.state != LevelState.GAME_OVER:
                        level_cfg = ServiceLocator.configs_service.get(
                            "assets/cfg/level_01.json")
                        ServiceLocator.sounds_service.play(
                            level_cfg["game_over_sound"])
                        c_lvl_mgr.state = LevelState.GAME_OVER
                        create_game_over_text(world)
