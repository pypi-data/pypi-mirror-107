# -*-coding: utf-8 -*-


import numpy as np
from sklearn.preprocessing import scale
from itertools import combinations

from castle.common import BaseLearner, Tensor
from castle.common.independence_tests import HSIC
from castle.algorithms.anm.utils.regressor import GPR


class ANM_Nonlinear(BaseLearner):
    """
    Nonlinear causal discovery with additive noise models

    Use GPML with Gaussian kernel and independent Gaussian noise,
    optimizing the hyper-parameters for each regression individually.
    For the independence test, we implemented the HSIC with a Gaussian kernel,
    where we used the gamma distribution as an approximation for the
    distribution of the HSIC under the null hypothesis of independence
    in order to calculate the p-value of the test result.

    References
    ----------
    Hoyer, Patrik O and Janzing, Dominik and Mooij, Joris M and Peters,
    Jonas and Schölkopf, Bernhard,
    "Nonlinear causal discovery with additive noise models", NIPS 2009

    Parameters
    ----------
    alpha : float, default 0.05
        significance level be used to compute threshold
    gpr_alpha : float or array-like of shape (n_samples), default=1e-10
        Value added to the diagonal of the kernel matrix during fitting.
        Larger values correspond to increased noise level in the observations.
        This can also prevent a potential numerical issue during fitting, by
        ensuring that the calculated values form a positive definite matrix.
        If an array is passed, it must have the same number of entries as the
        data used for fitting and is used as datapoint-dependent noise level.
        Note that this is equivalent to adding a WhiteKernel with c=alpha.
        Allowing to specify the noise level directly as a parameter is mainly
        for convenience and for consistency with Ridge.
    kernel : kernel instance, default=None
        The kernel specifying the covariance function of the GP. If None is
        passed, the kernel "1.0 * RBF(1.0)" is used as default. Note that
        the kernel's hyperparameters are optimized during fitting.

    Attributes
    ----------
    causal_matrix : array like shape of (n_features, n_features)
        Learned causal structure matrix.

    Examples
    --------
    Simplest Use
    >>> from castle.common import GraphDAG
    >>> from castle.metrics import MetricsDAG
    >>> from castle.datasets import DAG, IIDSimulation
    >>> from castle.algorithms import ANM_Nonlinear

    >>> weighted_random_dag = DAG.erdos_renyi(n_nodes=6, n_edges=10,
    >>>                                      weight_range=(0.5, 2.0), seed=1)
    >>> dataset = IIDSimulation(W=weighted_random_dag, n=1000,
    >>>                         method='nonlinear', sem_type='gp-add')
    >>> true_dag, X = dataset.B, dataset.X

    >>> anm = ANM_Nonlinear(alpha=0.05)
    >>> anm.learn(data=X)

    >>> # plot predict_dag and true_dag
    >>> GraphDAG(anm.causal_matrix, true_dag, 'result')

    you can also provide more parameters to use it. like the flowing:
    >>> from sklearn.gaussian_process.kernels import Matern, RBF
    >>> kernel = Matern(nu=1.5)
    >>> # kernel = 1.0 * RBF(1.0)
    >>> anm = ANM_Nonlinear(alpha=0.05, gpr_alpha=1e-10, kernel=kernel)
    >>> anm.learn(data=X)
    >>> # plot predict_dag and true_dag
    >>> GraphDAG(anm.causal_matrix, true_dag, 'result')
    """

    def __init__(self, alpha=0.05, **kwargs):
        super(ANM_Nonlinear, self).__init__()
        self.alpha = alpha
        self.kwargs = kwargs

    def learn(self, data, *args, **kwargs):
        """Set up and run the ANM_Nonlinear algorithm.

        Parameters
        ----------
        data: numpy.ndarray or Tensor
            Training data.
        regressor: Class instance
            class of regression method, if not provided, it is GPR.
        test_method: Class instance
            independence test method, if not provided, it is HSIC.
            The method named `test` must be implemented, accepts only
            two parameters x and y for independence test.
        """

        # create learning model and ground truth model
        if isinstance(data, np.ndarray):
            data = data
        elif isinstance(data, Tensor):
            data = data.data
        else:
            raise TypeError('The type of tensor must be '
                            'Tensor or numpy.ndarray, but got {}'
                            .format(type(data)))

        node_num = data.shape[1]
        self.causal_matrix = np.zeros((node_num, node_num))

        regressor = kwargs.get('regressor')
        test_method = kwargs.get('test_method')
        if regressor is None:
            gpr_alpha = self.kwargs.get('gpr_alpha', 1e-10)
            kernel = self.kwargs.get('kernel')
            regressor = GPR(alpha=gpr_alpha, kernel=kernel)
        if test_method is None:
            test_method = HSIC(alpha=self.alpha)

        for i, j in combinations(range(node_num), 2):
            x = data[:, i].reshape((-1, 1))
            y = data[:, j].reshape((-1, 1))

            flag = test_method.test(x, y)
            if flag == 1:
                continue
            # test x-->y
            flag = self.anm_estimate(x, y, regressor=regressor,
                                     test_method=test_method)
            if flag:
                self.causal_matrix[i, j] = 1
            # test y-->x
            flag = self.anm_estimate(y, x, regressor=regressor,
                                     test_method=test_method)
            if flag:
                self.causal_matrix[j, i] = 1

    def anm_estimate(self, x, y, regressor=GPR, test_method=HSIC):
        """Compute the fitness score of the ANM model in the x->y direction.

        Parameters
        ----------
        x: array
            Variable seen as cause
        y: array
            Variable seen as effect
        regressor: class object, default GPR
            Nonlinear regression estimator
        test_method: class object, default HSIC
            Independence test method like HSIC

        Returns
        -------
        out: int, 0 or 1
            If 1, residuals n is independent of x, then accept x --> y
            If 0, residuals n is not independent of x, then reject x --> y
        """

        x = scale(x).reshape((-1, 1))
        y = scale(y).reshape((-1, 1))

        y_predict = regressor.estimate(x, y)
        flag = test_method.test(y - y_predict, x)

        return flag

