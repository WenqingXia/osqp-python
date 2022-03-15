import osqp
from osqp.tests.utils import load_high_accuracy, rel_tol, abs_tol, decimal_tol, SOLVER_TYPES
import numpy as np
from scipy import sparse
import scipy as sp

import pytest
import numpy.testing as nptest


@pytest.fixture(params=SOLVER_TYPES)
def self(request):
    sp.random.seed(4)

    self.n = 30
    self.m = 0
    P = sparse.diags(np.random.rand(self.n)) + 0.2 * sparse.eye(self.n)
    self.P = P.tocsc()
    self.q = np.random.randn(self.n)
    self.A = sparse.csc_matrix((self.m, self.n))
    self.l = np.array([])
    self.u = np.array([])
    self.opts = {'verbose': False,
                 'eps_abs': 1e-08,
                 'eps_rel': 1e-08,
                 'polish': False}
    self.model = osqp.OSQP()
    self.model.setup(P=self.P, q=self.q, A=self.A, l=self.l, u=self.u,
                     **self.opts)
    return self


def test_unconstrained_problem(self):

    # Solve problem
    res = self.model.solve()

    # Assert close
    x_sol, _, obj_sol = load_high_accuracy('test_unconstrained_problem')
    # Assert close
    nptest.assert_allclose(res.x, x_sol, rtol=rel_tol, atol=abs_tol)
    nptest.assert_almost_equal(
        res.info.obj_val, obj_sol, decimal=decimal_tol)
