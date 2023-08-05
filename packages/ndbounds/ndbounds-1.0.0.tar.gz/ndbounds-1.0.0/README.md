# ndbounds

Toolbox for handling n-dimensional bounds.

## n-Dimensional Bounds

This is a format to combine methods for working with boundaries in
* 1D (e.g. onset & end of waveforms),
* 2D (e.g. bounding boxes in an image) or
* any higher nD case.

The basic idea of the format is, to store the bounds in an array organized as follows:

    [[start dim 1, end dim 1],
     [start dim 2, end dim 2],
     ...,
     [start dim n, end dim n]]