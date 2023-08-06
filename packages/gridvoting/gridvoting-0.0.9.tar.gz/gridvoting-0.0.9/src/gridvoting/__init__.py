import numpy as np
import cupy as cp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.spatial.distance import cdist


class Grid:
    def __init__(self, *, x0, x1, xstep=1, y0, y1, ystep=1):
        """initializes 2D grid with x0<=x<=x1 and y0<=y<=y1;
        Creates a 1D numpy array of grid coordinates in self.x and self.y"""
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.xstep = xstep
        self.ystep = ystep
        xvals = np.arange(x0, x1+xstep, xstep)
        yvals = np.arange(y1, y0-ystep, -ystep)
        xgrid, ygrid = np.meshgrid(xvals, yvals)
        self.x = np.ravel(xgrid)
        self.y = np.ravel(ygrid)
        self.extent = (self.x0, self.x1, self.y0, self.y1)
        self.gshape = (1+int((x1-x0)/xstep), 1+int((y1-y0)/ystep))
        self.len = self.gshape[0]*self.gshape[1]
        assert(self.x.shape == (self.len,))
        assert(self.y.shape == (self.len,))

    def as_xy_vectors(self):
        """returns [x,y] vectors for all grid points"""
        return np.column_stack((self.x, self.y))

    def index(self, *, x, y):
        """returns the unique 1D array index for grid point (x,y)"""
        isSelectedPoint = (self.x == x) & (self.y == y)
        indexes = np.flatnonzero((isSelectedPoint))
        assert(len(indexes) == 1)
        return indexes[0]

    def spatial_utilities(
        self,
        *,
        voter_ideal_points,
        metric='sqeuclidean',
        scale=-1
    ):
        """returns utility function values for each voter at each grid point"""
        return scale*cdist(
            voter_ideal_points,
            self.as_xy_vectors(),
            metric=metric
        )

    def plot(
        self,
        z,
        *,
        title=None,
        cmap=cm.gray_r,
        alpha=0.6,
        alpha_points=0.3,
        log=True,
        points=None,
        border=1,
        zoom=False,
        figsize=(10, 10)
    ):
        """plots values z defined on the grid;
        optionally plots additional 2D points
         and zooms to fit the bounding box of the points"""
        plt.figure(figsize=figsize)
        plt.rcParams["font.size"] = "24"
        if zoom:
            assert(points.shape[0] > 2)
            assert(points.shape[1] == 2)
            [min_x, min_y] = np.min(points, axis=0)-border
            [max_x, max_y] = np.max(points, axis=0)+border
            inZoom = (self.x >= min_x) & (self.x <= max_x) \
                & (self.y >= min_y) & (self.y <= max_y)
            zshape = (
                1+int((max_y-min_y)/self.ystep),
                1+int((max_x-min_x)/self.xstep)
            )
            extent = (min_x, max_x, min_y, max_y)
            zraw = np.copy(z[inZoom]).reshape(zshape)
            x = np.copy(self.x[inZoom]).reshape(zshape)
            y = np.copy(self.y[inZoom]).reshape(zshape)
        else:
            zshape = self.gshape
            extent = self.extent
            zraw = z.reshape(zshape)
            x = self.x.reshape(zshape)
            y = self.y.reshape(zshape)
        zplot = np.log10((1e-20)+zraw) if log else zraw
        contours = plt.contour(x, y, zplot, extent=extent, cmap=cmap)
        plt.clabel(contours, inline=True, fontsize=12, fmt='%1.2f')
        plt.imshow(zplot, extent=extent, cmap=cmap, alpha=alpha)
        if points is not None:
            plt.scatter(
                points[:, 0],
                points[:, 1],
                alpha=alpha_points,
                color='black'
            )
        if title is not None:
            plt.title(title)
        plt.show()


class MarkovChainGPU():
    def __init__(self, *, P, computeNow=True):
        """initializes a MarkovChainGPU instance by
         copying in the transition matrix P and calculating chain properties"""
        self.P = cp.asarray(P)  # copy transition matrix to cudapy as necessary
        assert(self.P.shape[0] == self.P.shape[1])  # matrix must be square
        diagP = cp.diagonal(self.P)
        self.absorbing_points = cp.equal(diagP, 1.0)
        self.unreachable_points = cp.equal(cp.sum(self.P, axis=0), diagP)
        self.has_unique_stationary_distibution = \
            not cp.any(self.absorbing_points)
        if computeNow and self.has_unique_stationary_distibution:
            self.find_unique_stationary_distribution()

    def find_unique_stationary_distribution(
        self,
        *,
        tolerance=1e-10,
        start_power=2
    ):
        """finds the stationary distribution for a Markov Chain by
        taking a sufficiently high power of the transition matrix"""
        if cp.any(self.absorbing_points):
            self.stationary_distribution = None
            return None
        unconverged = True
        check1 = 0  # upper left when P is from a grid
        check2 = int(self.P.shape[0]/2)  # center when P is from a grid
        power = start_power
        cP = self.P
        cP_LT = cp.linalg.matrix_power(cP, start_power)
        diags = {
            'power': [],
            'sum1minus1': [],
            'sum2minus1': [],
            'sad': [],
            'diff1': [],
            'diff2': []
        }
        while unconverged:
            cP_LT = cp.linalg.matrix_power(cP_LT, 2)
            power = power * 2
            row1 = cP_LT[check1]
            row2 = cP_LT[check2]
            # cast to float is required because cp.sum yields a cp.cparray
            # with zero dimensions instead of a scalar
            #
            # sum_..._ces = L1 norm of two different rows of P^power
            sum_absolute_differences = float(cp.sum(cp.abs(row1 - row2)))
            # diff1 = L1 norm of 1-step evolved row1 minus itself
            diff1 = float(cp.sum(cp.abs(cp.dot(row1, cP) - row1)))
            # diff2 = L1 norm of 1-step evolved row2 minus itself
            diff2 = float(cp.sum(cp.abs(cp.dot(row2, cP) - row2)))
            # sum1 = sum of row1, which should be 1.0
            sum1 = float(cp.sum(row1))
            # sum2 = sum of row2, which should be 1.0
            sum2 = float(cp.sum(row2))
            diags['sad'].append(sum_absolute_differences)
            diags['power'].append(power)
            diags['diff1'].append(diff1)
            diags['diff2'].append(diff2)
            diags['sum1minus1'].append(sum1-1.0)
            diags['sum2minus1'].append(sum2-1.0)
            unconverged = (sum_absolute_differences > tolerance)
        self.stationary_distribution = cp.copy(row1 if diff1 < diff2 else row2)
        self.power = power
        self.stationary_diagnostics = diags
        del cP_LT
        return self.stationary_distribution


class VotingModel():
    def __init__(
        self,
        *,
        utility_functions,
        number_of_voters,
        number_of_feasible_alternatives,
        majority,
        zi
    ):
        """initializes a VotingModel with utility_functions for each voter,
        the number_of_voters,
        the number_of_feasible_alternatives,
        the majority size, and whether to use zi (fully random) or
        intelligent challenges (random over winning set+status quo)"""
        assert(
            utility_functions.shape ==
            (number_of_voters, number_of_feasible_alternatives)
        )
        self.utility_functions = utility_functions
        self.number_of_voters = number_of_voters
        self.number_of_feasible_alternatives = number_of_feasible_alternatives
        self.majority = majority
        self.zi = zi
        self.analyzed = False

    def analyze(self):
        self.MarkovChain = MarkovChainGPU(P=self._get_transition_matrix())
        self.core_points = cp.asnumpy(self.MarkovChain.absorbing_points)
        self.core_exists = np.any(self.core_points)
        if not self.core_exists:
            self.stationary_distribution = \
                cp.asnumpy(self.MarkovChain.stationary_distribution)
        self.analyzed = True

    def what_beats(self, *, index):
        """returns array of size number_of_feasible_alternatives
        with value 1 where alternative beats current index by some majority"""
        assert(self.analyzed)
        points = cp.asnumpy(self.MarkovChain.P[index, :] > 0).astype('int')
        points[index] = 0
        return points

    def what_is_beaten_by(self, *, index):
        """returns array of size number_of_feasible_alternatives
        with value 1 where current index beats altetnative by some majority"""
        assert(self.analyzed)
        points = cp.asnumpy(self.MarkovChain.P[:, index] > 0).astype('int')
        points[index] = 0
        return points

    def plots(
        self,
        *,
        grid,
        voter_ideal_points,
        diagnostics=False,
        title_core='Core (aborbing) points',
        title_sad='L1 norm of difference in two rows of P^power',
        title_diff1='L1 norm of change in row1 (grid corner)',
        title_diff2='L1 norm of change in middle row (grid center)',
        title_sum1minus1='Sum of row1 (grid corner), minus 1.0',
        title_sum2minus1='Sum of middle row (grid center), minus 1.0',
        title_unreachable_points='Dominated (unreachable) points',
        title_stationary_distribution_no_grid='Stationary Distribution',
        title_stationary_distribution='Stationary Distribution',
        title_stationary_distribution_zoom='Stationary Distribution (zoom)'
    ):
        if self.core_exists:
            print("core plot")
            grid.plot(
                self.core_points.astype('int'),
                points=voter_ideal_points,
                zoom=True,
                title=title_core
            )
            return
        if diagnostics:
            df = pd.DataFrame(self.MarkovChain.stationary_diagnostics)
            df.plot.scatter('power', 'sad', loglog=True, title=title_sad)
            df.plot.scatter('power', 'diff1', loglog=True, title=title_diff1)
            df.plot.scatter('power', 'diff2', loglog=True, title=title_diff2)
            df.plot.scatter('power', 'sum1minus1', title=title_sum1minus1)
            df.plot.scatter('power', 'sum2minus1', title=title_sum2minus1)
            if grid is not None:
                grid.plot(
                    cp
                    .asnumpy(self.MarkovChain.unreachable_points)
                    .astype('int'),
                    title=title_unreachable_points
                )
        z = self.stationary_distribution
        if grid is None:
            pd.Series(z).plot(title=title_stationary_distribution_no_grid)
        else:
            grid.plot(
                z,
                points=voter_ideal_points,
                title=title_stationary_distribution
            )
            if voter_ideal_points is not None:
                grid.plot(
                    z,
                    points=voter_ideal_points,
                    zoom=True,
                    title=title_stationary_distribution_zoom
                )

    def _get_transition_matrix(self):
        utility_functions = self.utility_functions
        majority = self.majority
        zi = self.zi
        nfa = self.number_of_feasible_alternatives
        cV = cp.zeros(shape=(nfa, nfa), dtype=int)
        cU = cp.asarray(utility_functions)
        for a in range(nfa):
            total_votes_for_challenger_when_status_quo_is_a = \
                cp.greater(cU, cU[:, a, cp.newaxis]).astype('int').sum(axis=0)
            total_votes_shape = \
                total_votes_for_challenger_when_status_quo_is_a.shape
            assert(total_votes_shape == (nfa,))
            cV[a] = cp.greater_equal(
                total_votes_for_challenger_when_status_quo_is_a,
                majority
            ).astype('int')
        cp.testing.assert_array_equal(
            cp.diagonal(cV),
            cp.zeros(shape=(nfa), dtype=int)
        )
        cV_sum_of_row = cV.sum(axis=1)
        assert(cV_sum_of_row.shape == (nfa,))
        # diagonal will be set to reflect count of the losing challengers,
        # and self-challenge, equally likely with winning challengers
        if zi:
            cP = cp.divide(
                cp.add(
                    cV,
                    cp.diag(cp.subtract(nfa, cV_sum_of_row))
                ),
                nfa
            )
        else:
            cP = cp.divide(
                cp.add(cV, cp.eye(nfa)),
                (1+cV_sum_of_row)[:, cp.newaxis]
            )
        cp.testing.assert_array_almost_equal(
            cP.sum(axis=1),
            cp.ones(shape=(nfa)), decimal=10
        )
        return cP
