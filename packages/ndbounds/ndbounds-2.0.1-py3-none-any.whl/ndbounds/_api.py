# Copyright (C) 2021 Matthias Nadig

import numpy as np

from ._bounds import _as_bounds
from ._bounds import NdBounds
from ._bounds import NdBoundsSE, NdBoundsCW


def as_bounds_se(bounds,
                 require_n_dims=None, assert_order=True):
    """
    Assemble NdBounds object from an array or converts NdBounds to correct subtype
        --> receives array of format (start, end) or converts NdBounds accordingly
    """
    return _as_bounds(bounds, NdBoundsSE,
                      require_n_dims=require_n_dims,
                      assert_order=assert_order)


def as_bounds_cw(bounds,
                 require_n_dims=None):
    """
    Assemble NdBounds object from an array or converts NdBounds to correct subtype
        --> receives array of format (center, width) or converts NdBounds accordingly
    """
    return _as_bounds(bounds, NdBoundsCW,
                      require_n_dims=require_n_dims)


def raise_if_not_ndbounds(bounds):
    """ Checks input type """
    if not isinstance(bounds, NdBounds):
        raise TypeError('Expected input of type \'NdBounds\', instead got \'{}\''.format(type(bounds)))
