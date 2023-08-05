# Copyright (C) 2021 Matthias Nadig

import numpy as np

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


def _as_bounds(bounds, target_class,
               require_n_dims=None, assert_order=True):
    # Proceed depending on input type
    if isinstance(bounds, (np.ndarray, list, tuple)):
        # Input is an array containing the bounds, wrap it by the NdBounds object
        bounds = np.asarray(bounds)

        # Assert bounds array to be of shape (..., n_dims, 2)
        if bounds.ndim < 3 or bounds.shape[-1] != 2:
            raise ValueError('Bounds array has bad shape: (..., n_dims, 2) != {}'.format(bounds.shape))

        # Assert n_dims to be of certain value (dimensionality of bounds themselves, not the bounds array)
        if require_n_dims is not None:
            if bounds.shape[-2] != require_n_dims:
                raise ValueError(
                    'Given bounds do not fulfil user requirements. ' +
                    'Requested {}-dimensional bounds, got n_dims = {}'.format(require_n_dims, bounds.shape[-2]))

        # Check order of start and end (only in case bounds of type start-end are required)
        if assert_order and target_class == NdBoundsSE:
            is_wrong_order = np.less(np.subtract(bounds[..., 1], bounds[..., 0]), 0)
            if is_wrong_order.any():
                str_count = '{} of {} bounds'.format(np.sum(is_wrong_order), is_wrong_order.size)
                raise ValueError('Bounds have wrong order: start > end for {}'.format(str_count))

        bounds = NdBounds(target_class(bounds))
    elif isinstance(bounds, NdBounds):
        # Input is already of type NdBounds, convert to correct subtype if necessary
        if isinstance(bounds, target_class):
            # Type is already good, no conversion necessary
            pass
        elif target_class == NdBoundsSE:
            # Convert to required type: start-end
            bounds = NdBounds(target_class(bounds.get_bounds_se()))
        elif target_class == NdBoundsCW:
            # Convert to required type: center-width
            bounds = NdBounds(target_class(bounds.get_bounds_cw()))
        else:
            raise RuntimeError('Child of NdBounds has unexpected type: {}'.format(type(bounds)))
    else:
        raise ValueError('Unexpected type of bounds: {}'.format(bounds))

    return bounds
