from functools import partial
from typing import Generator
from typing import Iterable
from typing import Iterator
from typing import Tuple
from typing import Union

import numpy as np
from skimage.transform import AffineTransform
from skimage.transform import downscale_local_mean
from skimage.transform import rotate
from skimage.transform import warp


def average_numpy_arrays(arrays: Union[Iterable[np.ndarray], np.ndarray]) -> np.ndarray:
    """
    Given an iterable of numpy arrays, calculate the pixel-wise average and return
    it in a numpy array. This will work for a single array as well, just in case...

    Parameters
    ----------
    arrays
        The arrays to be averaged

    Returns
    -------
    The average of the input arrays

    """
    arrays = [arrays] if isinstance(arrays, np.ndarray) else arrays
    count = 0  # This statement is here only to suppress an uninitialized variable warning
    output = None
    for count, array in enumerate(arrays):
        if output is None:
            output = np.array(array)
        else:
            if array.shape != output.shape:
                raise ValueError(
                    f"All arrays must be the same shape. "
                    f"Shape of initial array = {output.shape} "
                    f"Shape of current array = {array.shape}"
                )
            output += array
    if output is not None:
        return output / (count + 1)
    raise ValueError("data_arrays is empty")


def subtract_array_from_arrays(
    arrays: Union[Iterable[np.ndarray], np.ndarray],
    array_to_subtract: np.ndarray,
) -> Generator[np.ndarray, None, None]:
    """
    Subtract a single array from an iterable of arrays. This will work if
    a single array is used in lieu of an iterable as well.

    Parameters
    ----------
    arrays
        The arrays from which to subtract
    array_to_subtract
        The array to be subtracted

    Returns
    -------
    An generator of modified arrays

    """
    arrays = [arrays] if isinstance(arrays, np.ndarray) else arrays
    for array in arrays:
        if array.shape != array_to_subtract.shape:
            raise ValueError(
                f"All arrays must be the same shape. "
                f"Shape of subtraction array = {array_to_subtract.shape} "
                f"Shape of current array = {array.shape}"
            )
        yield array - array_to_subtract


def divide_arrays_by_array(
    arrays: Union[Iterable[np.ndarray], np.ndarray],
    array_to_divide_by: np.ndarray,
) -> Generator[np.ndarray, None, None]:
    """
     Divide an iterable of arrays by a single array. This will work if
    a single array is used in lieu of an iterable as well.

    Parameters
    ----------
    arrays
        The arrays to be divided
    array_to_divide_by
        The array ny which to divide

    Returns
    -------
    A generator of modified arrays

    """
    arrays = [arrays] if isinstance(arrays, np.ndarray) else arrays
    for array in arrays:
        if array.shape != array_to_divide_by.shape:
            raise ValueError(
                f"All arrays must be the same shape. "
                f"Shape of subtraction array = {array_to_divide_by.shape} "
                f"Shape of current array = {array.shape}"
            )
        yield array / array_to_divide_by


def _bin_array(array: np.ndarray, bin_factors: (int, int)) -> np.ndarray:
    """
    Bin an array by summation over an integral number of pixels in each dimension.

    Parameters
    ----------
    array
        The array to be binned
    bin_factors
        The bin factors for each axis, which must be integral divisors of each array dimension

    Returns
    -------
    The binned array

    """
    input_shape = array.shape
    if input_shape[0] % bin_factors[0] or input_shape[1] % bin_factors[1]:
        raise ValueError(
            "Array dimensions must be an integral multiple of the binning factor\n"
            f"Shape of array = {input_shape}, binning factors = {bin_factors}"
        )
    return downscale_local_mean(array, bin_factors)


def bin_arrays(
    arrays: Union[Iterable[np.ndarray], np.ndarray], bin_factors: (int, int)
) -> Iterator[np.ndarray]:
    """
    Bin an iterable of arrays by summation over an integral number of pixels in each dimension.

    Parameters
    ----------
    arrays
        The arrays to be binned
    bin_factors
        The bin factors for each axis, which must be integral divisors of each array dimension

    Returns
    -------
    An Iterator yielding the binned arrays

    """
    arrays = [arrays] if isinstance(arrays, np.ndarray) else arrays
    partial_bin = partial(_bin_array, bin_factors=bin_factors)
    return map(partial_bin, arrays)


def affine_transform_arrays(
    arrays: Union[Iterable[np.ndarray], np.ndarray],
    matrix: np.ndarray = None,
    scale: Union[Tuple[float, float], np.ndarray, float] = None,
    translation: Union[Tuple[float, float], np.ndarray, float] = None,
    rotation: float = None,
    shear: Union[Tuple[float, float], np.ndarray, float] = None,
    **kwargs,
) -> Iterator[np.ndarray]:
    """
    Transform an iterable of input arrays using a generalized affine transform operator.
    A transform matrix may be specified or separate parameters for scale, translation,
    rotation and shear may be specified instead. This method abstracts the use of the
    scikit-image affine transform, which may easily be replaced with one from scipy or
    another origin. If transform parameters are specified, they are applied in this order:
    shear, scale, rotation, translation

    Parameters
    ----------
    arrays
        The array(s) to be transformed
    matrix
        The transformation matrix to be used for the transform. If specified, none of
        [translation, rotation, or shear] may be used. Optional.
    Optional arguments
        If matrix is not specified, at least one of the following must be used:
            scale
                The scale factor to be applied in the transform: (Sx, Sy). If a scalar is used, the same
                value is applied to each axis.
            translation
                The translation to be applied in the transform: (Tx, Ty) in pixel units.
            rotation
                The rotation angle, in radians, to be applied to the transformation.
                A positive angle is counter-clockwise in a right handed coordinate system
            shear:
                The shear factor to be applied in the transform: (Shx, Shy). If a scalar is used, the same
                value is applied to each axis.
            **kwargs
                Optional arguments to be passed on to skimage.transform.warp() if desired. See
                https://scikit-image.org/docs/stable/api/skimage.transform.html#skimage.transform.warp
                for more details.

    Returns
    -------
    The transformed array(s)

    """
    tform = None
    any_param_set = any(param is not None for param in [scale, translation, rotation, shear])
    if not any_param_set and matrix is None:
        raise ValueError(
            "You must specify matrix or at least one of scale, rotate, shear, or shift."
        )
    elif any_param_set and matrix is not None:
        raise ValueError(
            "You cannot specify both matrix and any of scale, rotate, shear, or shift."
        )
    elif matrix is not None:
        if matrix.shape != (3, 3):
            raise ValueError(f"Invalid shape of transformation matrix: {matrix.shape}")
        tform = AffineTransform(matrix=matrix)
    elif any_param_set:
        if scale is None:
            scale = (1.0, 1.0)
        elif np.isscalar(scale):
            scale = (scale, scale)
        if translation is None:
            translation = (0.0, 0.0)
        elif np.isscalar(translation):
            translation = (translation, translation)
        if rotation is None:
            rotation = 0.0
        if shear is None:
            shear = (0.0, 0.0)
        shear_mat = shear_matrix(shear)
        temp_tform = AffineTransform(scale=scale, translation=translation, rotation=rotation)
        tform_mat = temp_tform.params @ shear_mat
        tform = AffineTransform(matrix=tform_mat)
    arrays = [arrays] if isinstance(arrays, np.ndarray) else arrays
    partial_warp = partial(warp, inverse_map=tform.inverse, **kwargs)
    return map(partial_warp, arrays)


def rotate_arrays_about_point(
    arrays: Union[Iterable[np.ndarray], np.ndarray],
    angle: float = 0.0,
    point: Union[Tuple[float, float], np.ndarray] = None,
    **kwargs,
) -> Iterator[np.ndarray]:
    """
    Rotate an iterable of arrays about a specified point

    Parameters
    ----------
    arrays
        The array(s) to be rotated
    angle
        The angle, in radians, for the rotation to be applied, optional. Default is zero
        A positive angle is counter-clockwise in a right handed coordinate system and
        clockwise in a left-handed coordinate system
    point
        The point, in pixel coordinates (x, y) about which to rotate. Optional. Default is None,
        meaning the center of the array will be used. Note that the origin pixel is centered at
        (0, 0) and has extent: [-0.5: 0.5, -0.5: 0.5]
    kwargs
        Any arguments to be passed to skimage.transform.rotate. See
        https://scikit-image.org/docs/stable/api/skimage.transform.html#skimage.transform.rotate
        for more details.

    Returns
    -------
    An Iterator yielding the rotated arrays.

    """
    arrays = [arrays] if isinstance(arrays, np.ndarray) else arrays
    partial_rotate = partial(rotate, angle=np.degrees(angle), center=point, **kwargs)
    return map(partial_rotate, arrays)


def translate_arrays(
    arrays: Union[Iterable[np.ndarray], np.ndarray],
    translation: Union[Tuple[float, float], np.ndarray] = (0.0, 0.0),
    **kwargs,
) -> Iterator[np.ndarray]:
    """
    Translate an iterable of arrays by a specified vector

    Parameters
    ----------
    arrays
        The array(s) to be translated
    translation
        The translation to be applied in the transform: (Tx, Ty) in pixel units. Optional.
    **kwargs
        Optional arguments to be passed on to skimage.transform.warp() if desired. See
        https://scikit-image.org/docs/stable/api/skimage.transform.html#skimage.transform.warp
        for more details.

    Returns
    -------
    np.ndarray
        The translated array

    """
    arrays = [arrays] if isinstance(arrays, np.ndarray) else arrays
    return affine_transform_arrays(arrays, translation=translation, **kwargs)


def scale_matrix(scale_factors: Union[Tuple[float, float], float] = (1.0, 1.0)) -> np.ndarray:
    """
    Create an Affine Transform matrix for a scale operation

    Parameters
    ----------
    scale_factors
        The scale factors to use in scaling the array. If a scalar is passed, it
        is applied to both axes.
    Returns
    -------
    A 3x3 homogeneous transform matrix implementing the scaling
    """
    return AffineTransform(scale=scale_factors).params


def rotation_matrix(angle: float) -> np.ndarray:
    """
    Create an Affine Transform matrix for a rotation operation
    This assumes the rotation is about (0, 0) and it is up to the user
    to calculate the appropriate translation offset to be applied in the
    skimage.warp() method to achieve rotation about an arbitrary point

    Parameters
    ----------
    angle
        The angle of rotation in radians. This represents counter-clockwise rotation
        in a right-handed coordinate system and clockwise rotation in a left-handed
        system

    Returns
    -------
    A 3x3 homogeneous transform matrix implementing the rotation
    """
    return AffineTransform(rotation=angle).params


def shear_matrix(shear_factors: Union[Tuple[float, float], float] = (1.0, 1.0)) -> np.ndarray:
    """
    Create an Affine Transform matrix for a shear operation

    Parameters
    ----------
    shear_factors
        The shear scaling factors.

    Returns
    -------
    A 3x3 homogeneous transform matrix implementing the shear
    """
    if isinstance(shear_factors, float):
        shear_factors = shear_factors, shear_factors
    shear_mat = np.eye(3, 3)
    shear_mat[0, 1] = shear_factors[0]
    shear_mat[1, 0] = shear_factors[1]
    return shear_mat


def translation_matrix(offsets: Union[Tuple[float, float], float] = (1.0, 1.0)) -> np.ndarray:
    """
    Create an Affine Transform matrix for a translation operation

    Parameters
    ----------
    offsets
        The translation ofsets.

    Returns
    -------
    A 3x3 homogeneous transform matrix implementing the translation
    """
    if isinstance(offsets, float):
        offsets = offsets, offsets
    trans_mat = np.eye(3, 3)
    trans_mat[0, 2] = offsets[0]
    trans_mat[1, 2] = offsets[1]
    return trans_mat
