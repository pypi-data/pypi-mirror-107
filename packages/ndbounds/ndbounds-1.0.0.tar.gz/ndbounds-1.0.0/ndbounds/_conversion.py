# Copyright (C) 2021 Matthias Nadig

import numpy as np


def _convert_se_to_cw(bounds):
    """
    Convert from (start, end) to (center, width)
    """

    bounds_new = np.empty(bounds.shape)
    bounds_new[..., 1] = np.subtract(bounds[..., 1], bounds[..., 0], out=bounds_new[..., 1])
    bounds_new[..., 0] = np.add(bounds[..., 0], np.multiply(0.5, bounds_new[..., 1]), out=bounds_new[..., 0])

    return bounds_new


def _convert_cw_to_se(bounds):
    """
    Convert from (center, width) to (start, end)
    """

    bounds_new = np.empty(bounds.shape)

    bounds_center = np.copy(bounds[..., 0])
    bounds_size_half = np.multiply(0.5, bounds[..., 1])

    bounds_new[..., 0] = np.subtract(bounds_center, bounds_size_half)
    bounds_new[..., 1] = np.add(bounds_center, bounds_size_half)

    return bounds_new


def _convert_se_to_cw_inplace(bounds):
    """
    Convert from (start, end) to (center, width)
    CAVEAT: Inplace modification!
    """

    np.subtract(bounds[..., 1], bounds[..., 0], out=bounds[..., 1])
    np.add(bounds[..., 0], np.multiply(0.5, bounds[..., 1]), out=bounds[..., 0])

    return bounds


def _convert_cw_to_se_inplace(bounds):
    """
    Convert from (center, width) to (start, end)
    CAVEAT: Inplace modification!
    """

    bounds_center = np.copy(bounds[..., 0])
    bounds_size_half = np.multiply(0.5, bounds[..., 1], out=bounds[..., 1])

    np.subtract(bounds_center, bounds_size_half, out=bounds[..., 0])
    np.add(bounds_center, bounds_size_half, out=bounds[..., 1])

    return bounds
