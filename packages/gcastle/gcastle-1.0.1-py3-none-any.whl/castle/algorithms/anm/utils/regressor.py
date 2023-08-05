# -*-coding: utf-8 -*-

from sklearn.gaussian_process import GaussianProcessRegressor


class GPR(object):
    """Gaussian Process Regressor

    If you need to use other regression methods, you can define it, but must
    implement the `estimate` method.
    """

    def __init__(self, alpha=1e-10, **kwargs):
        self.alpha = alpha
        self.kwargs = kwargs

    def estimate(self, x, y):
        """regression estimate

        Parameters
        ----------
        x : array
            Variable seen as cause
        y: array
            Variable seen as effect

        Returns
        -------
        y_predict: array
            regression predict values of x
        """

        gpr = GaussianProcessRegressor(alpha=self.alpha, **self.kwargs)
        gpr.fit(x, y)
        y_predict = gpr.predict(x)

        return y_predict
