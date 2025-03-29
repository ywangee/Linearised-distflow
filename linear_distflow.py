import numpy as np
import pandas as pd
from network import net, nbus, nbranch, fbus, tbus, R_final, X_final

def solve_linear_distflow():
    
    V = np.ones(nbus) 
    P_branch = np.zeros(nbranch)
    Q_branch = np.zeros(nbranch)
    
    # 收集节点注入功率
    P_inj = np.zeros(nbus)
    Q_inj = np.zeros(nbus)
    
    # 从网络中提取功率数据
    for idx, load in net.load.iterrows():
        bus_idx = load['bus']
        P_inj[bus_idx] -= load['p_mw']
        Q_inj[bus_idx] -= load['q_mvar']
    
    for idx, gen in net.gen.iterrows():
        bus_idx = gen['bus']
        P_inj[bus_idx] += gen['p_mw']
    
    for idx, storage in net.storage.iterrows():
        bus_idx = storage['bus']
        P_inj[bus_idx] += storage['p_mw']
    

    for branch in range(nbranch-1, -1, -1):
        to_bus = tbus[branch][0]
        P_branch[branch] = P_inj[to_bus]
        Q_branch[branch] = Q_inj[to_bus]
        
        for next_branch in range(nbranch):
            if fbus[next_branch][0] == to_bus:
                P_branch[branch] += P_branch[next_branch]
                Q_branch[branch] += Q_branch[next_branch]
    
 
    for branch in range(nbranch):
        from_bus = fbus[branch][0]
        to_bus = tbus[branch][0]
        
        V[to_bus] = V[from_bus] - (R_final[branch+1] * P_branch[branch] + 
                                   X_final[branch+1] * Q_branch[branch])
    
    return {
        'voltage': V,
        'branch_P': P_branch,
        'branch_Q': Q_branch
    }

if __name__ == "__main__":
  
    results = solve_linear_distflow()
    
    # 打印结果
    print("voltage:")
    for i, v in enumerate(results['voltage']):
        print(f"bus {i}: {v:.6f}")
    
    print("\nbranch power p:")
    for i, p in enumerate(results['branch_P']):
        print(f"branch {i}: {p:.6f}")
    
    print("\nbranch power q:")
    for i, q in enumerate(results['branch_Q']):
        print(f"branch {i}: {q:.6f}")