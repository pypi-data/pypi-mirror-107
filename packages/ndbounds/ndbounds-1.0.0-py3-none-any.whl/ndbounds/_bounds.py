# Copyright (C) 2021 Matthias Nadig

import numpy as np

from ._conversion import _convert_cw_to_se
from ._conversion import _convert_cw_to_se_inplace
from ._conversion import _convert_se_to_cw
from ._conversion import _convert_se_to_cw_inplace


class NdBounds:
    """
    n-Dimensional Bounds

    Basic format is:
        [[start dim 1, end dim 1],
         [start dim 2, end dim 2],
         ...,
         [start dim n, end dim n]]
    """

    def __init__(self, bounds):
        self._bound_handler = bounds

    def get_n_dims(self):
        """
        Returns the number of dimensions of the bounds
        (NOT OF THE NUMPY ARRAY ITSELF)
        """
        return self._bound_handler.get_n_dims()

    def get_shape(self):
        """ Returns the shape of the Numpy array that contains the bounds """
        return self._bound_handler.get_shape()

    def get_bounds_se(self):
        """ Returns the bounds in a Numpy array with format (start, end) """
        return self._bound_handler.get_bounds_se()

    def get_bounds_cw(self):
        """ Returns the bounds in a Numpy array with format (center, width) """
        return self._bound_handler.get_bounds_cw()

    def convert_to_se(self):
        """
        Makes sure, that the bounds are kept in format (start, end)
        Note: This method is meant for runtime improvements only, and
        can be called, before the bounds are retrieved in SE format
        multiple times.
        """
        if isinstance(self._bound_handler, NdBoundsSE):
            pass
        elif isinstance(self._bound_handler, NdBoundsCW):
            bounds = self._bound_handler.get_bounds_cw()
            _convert_cw_to_se_inplace(bounds)
            self._bound_handler = NdBoundsSE(bounds)
        else:
            raise RuntimeError(type(self._bound_handler))

        return self

    def convert_to_cw(self):
        """
        Makes sure, that the bounds are kept in format (center, width)
        Also see convert_to_se().
        """
        if isinstance(self._bound_handler, NdBoundsCW):
            pass
        elif isinstance(self._bound_handler, NdBoundsSE):
            bounds = self._bound_handler.get_bounds_se()
            _convert_se_to_cw_inplace(bounds)
            self._bound_handler = NdBoundsCW(bounds)
        else:
            raise RuntimeError(type(self._bound_handler))

        return self

    def scale_dimensions(self, factor_each_dim):
        """ Scales the dimensions, the bounds refer to """
        self._bound_handler.scale_dimensions(factor_each_dim)
        return self

    def scale_width(self, factor_each_dim):
        """ Scales the width of the individual bounds """
        self._bound_handler.scale_width(factor_each_dim)
        return self

    def add_offset(self, offset_each_dim):
        """ Adds offset to the individual bounds """
        self._bound_handler.add_offset(offset_each_dim)
        return self

    def check_within(self, point):
        """ Returns True or False for each of the bounds, depending on if the point lies within them """

        # Check input
        point = np.asarray(point)
        if point.ndim != 1 or point.shape[-1] != self.get_n_dims():
            raise ValueError('point needs to be {}-dimensional, '.format(self.get_n_dims()) +
                             'got point with shape {}'.format(point.shape))

        # Repeat to fit shape of bounds
        for index_axis, n_repeat in enumerate(self.get_shape()[:-2]):
            point = np.expand_dims(point, axis=index_axis)
            point = np.repeat(point, n_repeat, axis=index_axis)

        # Check if point is within start and end
        bounds = self.get_bounds_se()
        is_after_start = bounds[..., 0] <= point
        is_before_end = bounds[..., 1] >= point
        is_within_bounds = np.logical_and(is_after_start, is_before_end).all(axis=-1)

        return is_within_bounds


class BoundFormatHandler:
    """
    A class that serves as interface to the actual array of bounds
    """

    def __init__(self, bounds):
        self._bounds = bounds.astype(np.float)

    def get_n_dims(self):
        return self._bounds.shape[-2]

    def get_shape(self):
        return self._bounds.shape

    def get_bounds_se(self):
        return self._get_bounds_se()

    def get_bounds_cw(self):
        return self._get_bounds_cw()

    def scale_dimensions(self, factor_each_dim):
        factor_each_dim = self._reshape_input_for_application_to_each_bounds(factor_each_dim)
        return self._scale_dimensions(factor_each_dim)

    def scale_width(self, factor_each_dim):
        factor_each_dim = self._reshape_input_for_application_to_each_bounds(factor_each_dim)
        return self._scale_width(factor_each_dim)

    def add_offset(self, offset_each_dim):
        offset_each_dim = self._reshape_input_for_application_to_each_bounds(offset_each_dim)
        return self._add_offset(offset_each_dim)

    def _get_bounds_se(self):
        # Should be overwritten by child
        raise RuntimeError()

    def _get_bounds_cw(self):
        # Should be overwritten by child
        raise RuntimeError()

    def _set_bounds_from_se(self, bounds_se):
        # Should be overwritten by child
        raise RuntimeError()

    def _set_bounds_from_cw(self, bounds_cw):
        # Should be overwritten by child
        raise RuntimeError()

    def _add_offset(self, offset_each_dim):
        # Should be overwritten by child
        raise RuntimeError()

    def _reshape_input_for_application_to_each_bounds(self, arr):
        arr = np.asarray(arr)
        if arr.ndim == 1 and arr.shape[-1] == self.get_n_dims():
            # Repeat the array for each bounds
            for n_elements in reversed(self.get_shape()[:-2]):
                arr = np.repeat(arr[np.newaxis], n_elements, axis=0)
        elif arr.shape == self.get_shape()[:-1]:
            # Shape already as required for calculations
            pass
        else:
            raise ValueError('Bad shape for input array. Expected {}, got {}.'.format(
                '{} or {}'.format(self.get_shape()[-2:-1], self.get_shape()[:-1]),
                arr.shape
            ))

        return arr

    def _scale_dimensions(self, factor_each_dim):
        # Apply scaling factors
        bounds_se = self.get_bounds_se()
        bounds_se = np.multiply(bounds_se, factor_each_dim[..., np.newaxis], out=bounds_se)

        # Convert result
        self._set_bounds_from_se(bounds_se)

        return self

    def _scale_width(self, factor_each_dim):
        # Apply scaling factors
        bounds_cw = self.get_bounds_cw()
        np.multiply(bounds_cw[..., 1], factor_each_dim, out=bounds_cw[..., 1])

        # Convert result
        self._set_bounds_from_cw(bounds_cw)

        return self


class NdBoundsSE(BoundFormatHandler):
    """ Handler for the format (start, end) """

    def __init__(self, bounds):
        super().__init__(bounds)

    def _get_bounds_se(self):
        return self._bounds

    def _get_bounds_cw(self):
        return _convert_se_to_cw(self._bounds)

    def _set_bounds_from_se(self, bounds_se):
        self._bounds = bounds_se

    def _set_bounds_from_cw(self, bounds_cw):
        self._bounds = _convert_cw_to_se_inplace(bounds_cw)

    def _add_offset(self, offset_each_dim):
        np.add(self._bounds, offset_each_dim[..., np.newaxis], out=self._bounds)


class NdBoundsCW(BoundFormatHandler):
    """ Handler for the format (center, width) """

    def __init__(self, bounds):
        super().__init__(bounds)

    def _get_bounds_se(self):
        return _convert_cw_to_se(self._bounds)

    def _get_bounds_cw(self):
        return self._bounds

    def _set_bounds_from_se(self, bounds_se):
        self._bounds = _convert_se_to_cw_inplace(bounds_se)

    def _set_bounds_from_cw(self, bounds_cw):
        self._bounds = bounds_cw

    def _add_offset(self, offset_each_dim):
        np.add(self._bounds[..., 0], offset_each_dim, out=self._bounds[..., 0])
