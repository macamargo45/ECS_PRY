from typing import Callable
from src.ecs.components.c_manager_level import LevelState
from src.ecs.components.c_manager_level import CManagerLevel
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.c_input_command import CInputCommand
import esper

from src.ecs.components.c_enemy_state import CEnemyState, EnemyStates
from src.ecs.components.c_transform import CTransform

def system_enemies_terminated(world:esper.World, c_manager_level: CManagerLevel):
    if c_manager_level.state == LevelState.PLAY:
        components = world.get_components(CSurface, CTagEnemy)
        hayEnemigos = False
        for _,(c_s, c_es) in components:
            hayEnemigos = True

        if not hayEnemigos:
            c_manager_level.state = LevelState.NEXT_LEVEL