# -*- coding: utf-8 -*-
"""Provides `EllipsesDataset`."""
import numpy as np
from odl.discr.lp_discr import uniform_discr
from odl.phantom import ellipsoid_phantom
from dival.datasets.dataset import GroundTruthDataset


class EllipsesDataset(GroundTruthDataset):
    """Dataset with images of multiple random ellipses.

    This dataset uses the function `odl.phantom.ellipsoid_phantom` to create
    the images.
    """
    def __init__(self):
        self.shape = (128, 128)
        self.len_train = 50000
        self.len_test = 5000

    def generator(self, test=False, min_pt=None, max_pt=None):
        """Yield random ellipse phantom images of shape (128, 128).

        Parameters
        ----------
        min_pt : [int, int], optional
            Minimum values of the lp space.
        max_pt : [int, int], optional
            Maximum values of the lp space.
        """
        if min_pt is None:
            min_pt = [-self.shape[0]/2, -self.shape[1]/2]
        if max_pt is None:
            max_pt = [self.shape[0]/2, self.shape[1]/2]
        space = uniform_discr(min_pt, max_pt, self.shape, dtype=np.float32)

        r = np.random.RandomState(1 if test else 42)
        n = self.len_test if test else self.len_train
        n_ellipse = 50
        ellipsoids = np.empty((n_ellipse, 6))
        for _ in range(n):
            v = (r.uniform(-.5, .5, (n_ellipse,)) *
                 r.exponential(.4, (n_ellipse,)))
            a1 = .2 * r.exponential(1., (n_ellipse,))
            a2 = .2 * r.exponential(1., (n_ellipse,))
            x = r.uniform(-1., 1., (n_ellipse,))
            y = r.uniform(-1., 1., (n_ellipse,))
            rot = r.uniform(0., 2*np.pi, (n_ellipse,))
            ellipsoids = np.stack((v, a1, a2, x, y, rot), axis=1)
            image = ellipsoid_phantom(space, ellipsoids)

            yield image
