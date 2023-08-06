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

    def get_bounds_se(self, copy=True):
        """ Returns the bounds in a Numpy array with format (start, end) """
        return self._bound_handler.get_bounds_se(copy=copy)

    def get_bounds_cw(self, copy=True):
        """ Returns the bounds in a Numpy array with format (center, width) """
        return self._bound_handler.get_bounds_cw(copy=copy)

    def get_center(self, copy=True):
        """ Returns the center of the bounds """
        return self._bound_handler.get_center(copy=copy)

    def get_width(self, copy=True):
        """ Returns the width of the bounds """
        return self._bound_handler.get_width(copy=copy)

    def get_start(self, copy=True):
        """ Returns the start of the bounds """
        return self._bound_handler.get_start(copy=copy)

    def get_end(self, copy=True):
        """ Returns the end of the bounds """
        return self._bound_handler.get_end(copy=copy)

    def convert_to_se(self, inplace=False):
        """
        Makes sure, that the bounds are kept in format (start, end)
        Note 1: This method is meant for runtime improvements only, and
        can be called, before the bounds are retrieved in SE format
        multiple times.
        Note 2: The inplace option refers to the underlying Numpy array,
        containing the bound information. Using the convert-method will
        always convert the NdBounds instance inplace.
        """
        if isinstance(self._bound_handler, NdBoundsSE):
            pass
        elif isinstance(self._bound_handler, NdBoundsCW):
            bounds = self._bound_handler.get_bounds_cw(copy=not inplace)
            bounds = _convert_cw_to_se_inplace(bounds)
            self._bound_handler = NdBoundsSE(bounds)
        else:
            raise RuntimeError(type(self._bound_handler))

        return self

    def convert_to_cw(self, inplace=False):
        """
        Makes sure, that the bounds are kept in format (center, width)
        Also see convert_to_se().
        """
        if isinstance(self._bound_handler, NdBoundsCW):
            pass
        elif isinstance(self._bound_handler, NdBoundsSE):
            bounds = self._bound_handler.get_bounds_se(copy=not inplace)
            bounds = _convert_se_to_cw_inplace(bounds)
            self._bound_handler = NdBoundsCW(bounds)
        else:
            raise RuntimeError(type(self._bound_handler))

        return self

    def scale_dimensions(self, factor_each_dim, inplace=False):
        """ Scales the dimensions, the bounds refer to """
        return self._bound_handler.scale_dimensions(factor_each_dim, inplace=inplace)

    def scale_width(self, factor_each_dim, inplace=False):
        """ Scales the width of the individual bounds """
        return self._bound_handler.scale_width(factor_each_dim, inplace=inplace)

    def add_offset(self, offset_each_dim, inplace=False):
        """ Adds offset to the individual bounds """
        return self._bound_handler.add_offset(offset_each_dim, inplace=inplace)

    def apply_func_on_position(self, fn, inplace=False):
        return self._bound_handler.apply_func_on_position(fn, inplace=inplace)

    def apply_func_on_width(self, fn, inplace=False):
        return self._bound_handler.apply_func_on_width(fn, inplace=inplace)

    def copy(self):
        """ Copies the bounds """
        return self._bound_handler.copy()

    def delete(self, indices, axis=None):
        return self._bound_handler.delete(indices, axis=axis)

    def __delitem__(self, key):
        del self._bound_handler[key]

    def __getitem__(self, key):
        return self._bound_handler[key]

    def __setitem__(self, key, value):
        self._bound_handler[key] = value

    def check_within(self, point):
        """ Returns True or False for each of the bounds, depending on if the point lies within them """

        # Check input
        point = np.asarray(point)
        if point.ndim != 1 or point.shape[-1] != self.get_n_dims():
            raise ValueError('point needs to be {}-dimensional, '.format(self.get_n_dims()) +
                             'got point with shape {}'.format(point.shape))

        # Repeat to fit shape of bounds
        for index_axis, n_repeat in enumerate(self.get_shape()):
            point = np.expand_dims(point, axis=index_axis)
            point = np.repeat(point, n_repeat, axis=index_axis)

        # Check if point is within start and end
        bounds = self.get_bounds_se(copy=False)
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
        return self._bounds.shape[:-2]

    def get_bounds_se(self, copy=True):
        return self._get_bounds_se(copy=copy)

    def get_bounds_cw(self, copy=True):
        return self._get_bounds_cw(copy=copy)

    def get_center(self, copy=True):
        return self._get_center(copy=copy)

    def get_width(self, copy=True):
        return self._get_width(copy=copy)

    def get_start(self, copy=True):
        return self._get_start(copy=copy)

    def get_end(self, copy=True):
        return self._get_end(copy=copy)

    def scale_dimensions(self, factor_each_dim, inplace=False):
        factor_each_dim = self._reshape_input_for_application_to_each_bounds(factor_each_dim)
        return self._scale_dimensions(factor_each_dim, inplace=inplace)

    def scale_width(self, factor_each_dim):
        factor_each_dim = self._reshape_input_for_application_to_each_bounds(factor_each_dim)
        return self._scale_width(factor_each_dim)

    def add_offset(self, offset_each_dim, inplace=False):
        offset_each_dim = self._reshape_input_for_application_to_each_bounds(offset_each_dim)
        return self._add_offset(offset_each_dim, inplace=inplace)

    def apply_func_on_position(self, fn, inplace=False):
        bounds_out = self.get_bounds_cw(copy=not inplace)
        fn(bounds_out[..., 0], out=bounds_out[..., 0])
        return _as_bounds(bounds_out, NdBoundsCW, assert_order=False)

    def apply_func_on_width(self, fn, inplace=False):
        bounds_out = self.get_bounds_cw(copy=not inplace)
        fn(bounds_out[..., 1], out=bounds_out[..., 1])
        return _as_bounds(bounds_out, NdBoundsCW, assert_order=False)

    def copy(self):
        return _as_bounds(np.copy(self._bounds), type(self), assert_order=False)

    def _get_bounds_se(self, copy=True):
        # Should be overwritten by child
        raise RuntimeError()

    def _get_bounds_cw(self, copy=True):
        # Should be overwritten by child
        raise RuntimeError()

    def _get_center(self, copy=True):
        # Should be overwritten by child
        raise RuntimeError()

    def _get_width(self, copy=True):
        # Should be overwritten by child
        raise RuntimeError()

    def _get_start(self, copy=True):
        # Should be overwritten by child
        raise RuntimeError()

    def _get_end(self, copy=True):
        # Should be overwritten by child
        raise RuntimeError()

    def _set_bounds_from_se(self, bounds_se):
        # Should be overwritten by child
        raise RuntimeError()

    def _set_bounds_from_cw(self, bounds_cw):
        # Should be overwritten by child
        raise RuntimeError()

    def _add_offset(self, offset_each_dim, inplace=False):
        # Should be overwritten by child
        raise RuntimeError()

    def _reshape_input_for_application_to_each_bounds(self, arr):
        arr = np.asarray(arr)
        if arr.shape == (self.get_n_dims(),):
            # Repeat the array for each bounds
            for n_elements in reversed(self.get_shape()):
                arr = np.repeat(arr[np.newaxis], n_elements, axis=0)
        elif arr.shape == self.get_shape()+(self.get_n_dims(),):
            # Shape already as required for calculations
            pass
        else:
            raise ValueError('Bad shape for input array. Expected {}, got {}.'.format(
                '{} or {}'.format((self.get_n_dims(),), self.get_shape()+(self.get_n_dims(),)),
                arr.shape
            ))

        return arr

    def _scale_dimensions(self, factor_each_dim, inplace=False):
        # Apply scaling factors
        bounds_se = self.get_bounds_se(copy=not inplace)
        bounds_se = np.multiply(bounds_se, factor_each_dim[..., np.newaxis], out=bounds_se)

        # Convert result when writing back into own bounds if necessary
        if inplace:
            self._set_bounds_from_se(bounds_se)
            target_class = type(self)
        else:
            target_class = NdBoundsSE

        return _as_bounds(bounds_se, target_class, assert_order=False)

    def _scale_width(self, factor_each_dim, inplace=False):
        # Apply scaling factors
        bounds_cw = self.get_bounds_cw(copy=not inplace)
        np.multiply(bounds_cw[..., 1], factor_each_dim, out=bounds_cw[..., 1])

        # Convert result when writing back into own bounds if necessary
        if inplace:
            self._set_bounds_from_cw(bounds_cw)
            target_class = type(self)
        else:
            target_class = NdBoundsCW

        return _as_bounds(bounds_cw, target_class, assert_order=False)

    def delete(self, indices, axis=None):
        if axis is None:
            bounds_new = np.reshape(self._bounds, (-1, self.get_n_dims(), 2))
            axis = 0
        elif axis > len(self.get_shape()):
            raise ValueError('Cannot delete elements along axis {} for bounds of shape {}'.format(
                axis, self.get_shape()+(self.get_n_dims(), 2)))
        else:
            bounds_new = self._bounds
        bounds_new = np.delete(bounds_new, indices, axis=axis)
        return _as_bounds(bounds_new, type(self), assert_order=False)

    def __delitem__(self, key):
        raise NotImplementedError('To delete single bounds, use the delete(...)-method')

    def __getitem__(self, key):
        return _as_bounds(self._bounds[key], type(self), require_n_dims=self.get_n_dims(), assert_order=False)

    def __setitem__(self, key, value):
        raise RuntimeError('Tried to modify bounds. Access by indexing is read-only.')


class NdBoundsSE(BoundFormatHandler):
    """ Handler for the format (start, end) """

    def __init__(self, bounds):
        super().__init__(bounds)

    def _get_bounds_se(self, copy=True):
        return _copy_if_required(self._bounds, copy=copy)

    def _get_bounds_cw(self, copy=True):
        bounds_out = _copy_if_required(self._bounds, copy=True)
        return _convert_se_to_cw_inplace(bounds_out)

    def _get_center(self, copy=True):
        bounds_out = _copy_if_required(self._bounds, copy=True)
        return _convert_se_to_cw_inplace(bounds_out)[..., 0]

    def _get_width(self, copy=True):
        bounds_out = _copy_if_required(self._bounds, copy=True)
        return _convert_se_to_cw_inplace(bounds_out)[..., 1]

    def _get_start(self, copy=True):
        return _copy_if_required(self._bounds, copy=copy)[..., 0]

    def _get_end(self, copy=True):
        return _copy_if_required(self._bounds, copy=copy)[..., 1]

    def _set_bounds_from_se(self, bounds_se):
        self._bounds = bounds_se
        return self

    def _set_bounds_from_cw(self, bounds_cw):
        self._bounds = _convert_cw_to_se_inplace(bounds_cw)
        return self

    def _add_offset(self, offset_each_dim, inplace=False):
        bounds_out = np.add(self._bounds, offset_each_dim[..., np.newaxis], out=self._bounds if inplace else None)
        return _as_bounds(bounds_out, NdBoundsSE, assert_order=False)


class NdBoundsCW(BoundFormatHandler):
    """ Handler for the format (center, width) """

    def __init__(self, bounds):
        super().__init__(bounds)

    def _get_bounds_se(self, copy=True):
        bounds_out = _copy_if_required(self._bounds, copy=True)
        return _convert_cw_to_se_inplace(bounds_out)

    def _get_bounds_cw(self, copy=True):
        return _copy_if_required(self._bounds, copy=copy)

    def _get_center(self, copy=True):
        return _copy_if_required(self._bounds, copy=copy)[..., 0]

    def _get_width(self, copy=True):
        return _copy_if_required(self._bounds, copy=copy)[..., 1]

    def _get_start(self, copy=True):
        bounds_out = _copy_if_required(self._bounds, copy=True)
        return _convert_cw_to_se_inplace(bounds_out)[..., 0]

    def _get_end(self, copy=True):
        bounds_out = _copy_if_required(self._bounds, copy=True)
        return _convert_cw_to_se_inplace(bounds_out)[..., 1]

    def _set_bounds_from_se(self, bounds_se):
        self._bounds = _convert_se_to_cw_inplace(bounds_se)
        return self

    def _set_bounds_from_cw(self, bounds_cw):
        self._bounds = bounds_cw
        return self

    def _add_offset(self, offset_each_dim, inplace=False):
        bounds_out_center = np.add(self._bounds[..., 0], offset_each_dim, out=self._bounds[..., 0] if inplace else None)
        bounds_out = self._bounds if inplace else np.stack([bounds_out_center, self._bounds[..., 1]], axis=-1)
        return _as_bounds(bounds_out, NdBoundsCW, assert_order=False)


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


def _copy_if_required(arr, copy):
    if copy:
        return np.copy(arr)
    else:
        return arr
