import esper

from src.ecs.components.c_enemy_state import CEnemyState, EnemyStates
from src.ecs.components.c_transform import CTransform

def system_enemy_state(world:esper.World):
    query = world.get_components(CEnemyState, CTransform)
    for _, (c_st, c_tr) in query:
        if c_st.state == EnemyStates.IDLE:
            enemy_idle(c_st, c_tr)
      
  
def enemy_idle(c_st:CEnemyState, c_tr:CTransform):
    c_tr.pos.x = c_st.move_pos.x
    c_tr.pos.y = c_st.move_pos.y
    
