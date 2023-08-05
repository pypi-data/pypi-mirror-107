if True:
        
    '''
    # 如需要保存日志到文件，可运行如下两行
    from loguru import logger
    logger.add('file.log', filter='', level='DEBUG', 
            format='{time:YYYY-MM-DD HH:mm:ss} {name}({line}) {level} {message}')

    # 在 服务器 运行可能会遇到【ImportError: dlopen: cannot load any more object with static TLS】
    # 在 import 前添加如下两行即可
    import torch
    from sklearn.preprocessing import StandardScaler
    '''

    import sys
    sys.path.append(r'D:\project\ywx5333176\pcastle')
    sys.path.append(r'/opt/home/yxy/project/ywx5333176/pcastle')

    import numpy as np
    import pandas as pd

    from castle.common import Tensor
    from castle.common import GraphDAG
    from castle.metrics import MetricsDAG
    from castle.datasets import DAG, IIDSimulation
    from castle.datasets import Topology, THPSimulation

    from castle.algorithms.pc import PC
    from castle.algorithms.lingam import DirectLiNGAM
    from castle.algorithms.lingam import ICALiNGAM
    from castle.algorithms.gradient.notears import Notears
    from castle.algorithms.gradient.notears import NotearsMLP
    from castle.algorithms.gradient.notears import NotearsSob
    from castle.algorithms.gradient.notears import NotearsLowRank
    from castle.algorithms.gradient.notears import GOLEM
    from castle.algorithms.gradient.graph_auto_encoder import GAE
    from castle.algorithms.gradient.gran_dag import GraN_DAG
    from castle.algorithms.gradient.masked_csl import MCSL
    from castle.algorithms.gradient.rl import RL
    from castle.algorithms.gradient.corl1 import CORL1
    from castle.algorithms.gradient.corl2 import CORL2
    from castle.algorithms.ttpm import TTPM


    #################################
    #### simulation data
    #################################
    # DAG, ER
    weighted_random_dag = DAG.erdos_renyi(n_nodes=10, n_edges=20, weight_range=(0.5, 2.0), seed=1)
    # DAG, SF
    weighted_random_dag = DAG.scale_free(n_nodes=10, n_edges=20, weight_range=(0.5, 2.0), seed=1)
    # DAG, bipartite
    weighted_random_dag = DAG.bipartite(n_nodes=10, n_edges=5, split_ratio=0.2, weight_range=(0.5, 2.0), seed=1)
    # DAG, hierarchical
    weighted_random_dag = DAG.hierarchical(n_nodes=10, degree=5, graph_level=5, weight_range=(0.5, 2.0), seed=1)
    # DAG, low_rank
    weighted_random_dag = DAG.low_rank(n_nodes=10, degree=2, rank=5, weight_range=(0.5, 2.0), seed=1)

    # linear-gauss
    dataset = IIDSimulation(W=weighted_random_dag, n=2000, method='linear', sem_type='gauss')
    # linear-exp
    dataset = IIDSimulation(W=weighted_random_dag, n=2000, method='linear', sem_type='exp')
    # linear-poisson
    weighted_random_dag = DAG.erdos_renyi(n_nodes=100, n_edges=5, weight_range=(0.5, 2.0), seed=1)
    dataset = IIDSimulation(W=weighted_random_dag, n=2000, method='linear', sem_type='poisson')
    # nonlinear-mlp
    dataset = IIDSimulation(W=weighted_random_dag, n=2000, method='nonlinear', sem_type='mlp')
    # nonlinear-quadratic
    dataset = IIDSimulation(W=weighted_random_dag, n=2000, method='nonlinear', sem_type='quadratic')




import torch
from sklearn.preprocessing import StandardScaler

import sys
sys.path.append(r'D:\project\ywx5333176\pcastle')
sys.path.append(r'/opt/home/yxy/project/ywx5333176/pcastle')

import numpy as np
import pandas as pd

from castle.common import Tensor
from castle.common import GraphDAG
from castle.metrics import MetricsDAG
from castle.datasets import DAG, IIDSimulation

from castle.algorithms.lingam import DirectLiNGAM
from castle.algorithms.lingam import ICALiNGAM

from castle.algorithms.gradient import Notears
from castle.algorithms.gradient import NotearsMLP
from castle.algorithms.gradient import NotearsSob
from castle.algorithms.gradient import NotearsLowRank
from castle.algorithms.gradient import GOLEM
from castle.algorithms.gradient import GAE
from castle.algorithms.gradient import GraN_DAG
from castle.algorithms.gradient import MCSL
from castle.algorithms.gradient import RL
from castle.algorithms.gradient import CORL1
from castle.algorithms.gradient import CORL2


weighted_random_dag = DAG.erdos_renyi(n_nodes=10, n_edges=20, weight_range=(0.5, 2.0), seed=1)
dataset = IIDSimulation(W=weighted_random_dag, n=2000, method='linear', sem_type='gauss')

true_dag, X = dataset.B, dataset.X
tensor = Tensor(X)

# DirectLiNGAM fit model
n = DirectLiNGAM()
n.learn(tensor)

# ICALiNGAM fit model
n = ICALiNGAM()
n.learn(tensor)

# plot est_dag and true_dag
GraphDAG(n.causal_matrix, true_dag)

# calculate accuracy
met = MetricsDAG(n.causal_matrix, true_dag)
print(met.metrics)




import torch
from sklearn.preprocessing import StandardScaler

    >>> from castle.algorithms import PC
    >>> from castle.common import GraphDAG
    >>> from castle.metrics import MetricsDAG
    >>> from castle.datasets import load_dataset
    >>> true_dag, X = load_dataset(name='iid_test')
    >>> pc = PC()
    >>> pc.learn(X)
    >>> met = MetricsDAG(pc.causal_matrix, true_dag)
    >>> print(met.metrics)

    >>> from castle.algorithms import GraN_DAG, Parameters
    >>> from castle.datasets import load_dataset
    >>> target, data = load_dataset(name='iid_test')
    >>> params = Parameters(input_dim=data.shape[1])
    >>> gnd = GraN_DAG(params=params)
    >>> gnd.learn(data=data, target=target)
    >>> print(gnd.model.metrics)
    >>> print(gnd.causal_matrix)
    >>> print(gnd.model.adjacency)


import torch
from sklearn.preprocessing import StandardScaler

    >>> from castle.common import GraphDAG
    >>> from castle.metrics import MetricsDAG
    >>> from castle.datasets import load_dataset
    >>> from castle.algorithms import TTPM
    >>> true_causal_matrix, topology_matrix, X = load_dataset(name='thp_test')
    >>> ttpm = TTPM(topology_matrix)
    >>> ttpm.learn(X, max_hop=2)
    >>> causal_matrix = ttpm.causal_matrix
    >>> ret_metrix = MetricsDAG(ttpm.causal_matrix.values, true_causal_matrix)
    >>> ret_metrix.metrics


import torch
from sklearn.preprocessing import StandardScaler
import numpy as np

    >>> from castle.common import GraphDAG
    >>> from castle.metrics import MetricsDAG
    >>> from castle.datasets import load_dataset
    >>> from castle.algorithms import DirectLiNGAM
    >>> true_dag, X = load_dataset(name='iid_test')
    >>> n = DirectLiNGAM()
    >>> n.learn(X)
    >>> met = MetricsDAG(n.causal_matrix, true_dag)
    >>> print(met.metrics)

    >>> from castle.algorithms import ICALiNGAM
    >>> true_dag, X = load_dataset(name='iid_test')
    >>> n = ICALiNGAM()
    >>> n.learn(X)
    >>> met = MetricsDAG(n.causal_matrix, true_dag)
    >>> print(met.metrics)

    >>> from castle.algorithms import GOLEM
    >>> true_dag, X = load_dataset(name='iid_test')
    >>> n = GOLEM()
    >>> n.learn(X, lambda_1=2e-2, lambda_2=5.0, equal_variances=True)
    >>> met = MetricsDAG(n.causal_matrix, true_dag)
    >>> print(met.metrics)

    >>> from castle.algorithms import Notears
    >>> true_dag, X = load_dataset(name='iid_test')
    >>> n = Notears()
    >>> n.learn(X)
    >>> met = MetricsDAG(n.causal_matrix, true_dag)
    >>> print(met.metrics)

    >>> from castle.algorithms import NotearsLowRank
    >>> true_dag, X = load_dataset(name='iid_test')
    >>> rank = np.linalg.matrix_rank(true_dag)
    >>> n = NotearsLowRank()
    >>> n.learn(X, rank=rank)
    >>> met = MetricsDAG(n.causal_matrix, true_dag)
    >>> print(met.metrics)

    >>> from castle.algorithms import NotearsMLP
    >>> true_dag, X = load_dataset(name='iid_test')
    >>> n = NotearsMLP()
    >>> n.learn(X)
    >>> met = MetricsDAG(n.causal_matrix, true_dag)
    >>> print(met.metrics)

    >>> from castle.algorithms import NotearsSob
    >>> true_dag, X = load_dataset(name='iid_test')
    >>> n = NotearsSob()
    >>> n.learn(X)
    >>> met = MetricsDAG(n.causal_matrix, true_dag)
    >>> print(met.metrics)

    >>> from castle.algorithms import GAE
    >>> true_dag, X = load_dataset(name='iid_test')
    >>> n = GAE()
    >>> n.learn(X, num_encoder_layers=2, num_decoder_layers=2, hidden_size=16,
                max_iter=20, h_tol=1e-12, iter_step=300, rho_thres=1e20, rho_multiply=10, 
                graph_thres=0.2, l1_graph_penalty=1.0, init_iter=5, use_float64=True)
    >>> met = MetricsDAG(n.causal_matrix, true_dag)
    >>> print(met.metrics)

    >>> from castle.algorithms import MCSL
    >>> true_dag, X = load_dataset(name='iid_test')
    >>> n = MCSL()
    >>> n.learn(X, iter_step=1000, rho_thres=1e14, init_rho=1e-5,
                rho_multiply=10, graph_thres=0.5, l1_graph_penalty=2e-3, 
                degree=2, use_float64=False)
    >>> met = MetricsDAG(n.causal_matrix, true_dag)
    >>> print(met.metrics)


import torch
from sklearn.preprocessing import StandardScaler

    >>> from castle.algorithms import RL
    >>> from castle.datasets import load_dataset
    >>> from castle.common import GraphDAG
    >>> from castle.metrics import MetricsDAG
    >>> true_dag, X = load_dataset(name='iid_test')
    >>> n = RL()
    >>> n.learn(X, dag=true_dag, lambda_flag_default=True)
    >>> met = MetricsDAG(n.causal_matrix, true_dag)
    >>> print(met.metrics)

    >>> from castle.algorithms import CORL1
    >>> from castle.datasets import load_dataset
    >>> from castle.common import GraphDAG
    >>> from castle.metrics import MetricsDAG
    >>> true_dag, X = load_dataset(name='iid_test')
    >>> n = CORL1()
    >>> n.learn(X, dag=true_dag)
    >>> met = MetricsDAG(n.causal_matrix, true_dag)
    >>> print(met.metrics)

    >>> from castle.algorithms import CORL2
    >>> from castle.datasets import load_dataset
    >>> from castle.common import GraphDAG
    >>> from castle.metrics import MetricsDAG
    >>> true_dag, X = load_dataset(name='iid_test')
    >>> n = CORL2()
    >>> n.learn(X, dag=true_dag)
    >>> met = MetricsDAG(n.causal_matrix, true_dag)
    >>> print(met.metrics)




