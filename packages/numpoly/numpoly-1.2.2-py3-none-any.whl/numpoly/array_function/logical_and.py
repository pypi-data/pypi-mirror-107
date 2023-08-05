"""Compute the truth value of x1 AND x2 element-wise."""
from __future__ import annotations
from typing import Any, Optional, Sequence, Union

import numpy
import numpoly

from ..baseclass import PolyLike
from ..dispatch import implements


@implements(numpy.logical_and)
def logical_and(
        x1: PolyLike,
        x2: PolyLike,
        out: Optional[numpy.ndarray] = None,
        where: Union[bool, Sequence[bool]] = True,
        **kwargs: Any,
) -> numpy.ndarray:
    """
    Compute the truth value of x1 AND x2 element-wise.

    Args:
        x1, x2
            Input arrays. If ``x1.shape != x2.shape``, they must be
            broadcastable to a common shape (which becomes the shape of the
            output).
        out:
            A location into which the result is stored. If provided, it must
            have a shape that the inputs broadcast to. If not provided or
            `None`, a freshly-allocated array is returned. A tuple (possible
            only as a keyword argument) must have length equal to the number of
            outputs.
        where:
            This condition is broadcast over the input. At locations where the
            condition is True, the `out` array will be set to the ufunc result.
            Elsewhere, the `out` array will retain its original value. Note
            that if an uninitialized `out` array is created via the default
            ``out=None``, locations within it where the condition is False will
            remain uninitialized.
        kwargs:
            Keyword args passed to numpy.ufunc.

    Returns:
        Boolean result of the logical OR operation applied to the elements of
        `x1` and `x2`; the shape is determined by broadcasting. This is a
        scalar if both `x1` and `x2` are scalars.

    Examples:
        >>> q0, q1 = numpoly.variable(2)
        >>> numpoly.logical_and(q0, 0)
        False
        >>> numpoly.logical_and([q0, False], [q0, q1])
        array([ True, False])
        >>> const = numpy.arange(5)
        >>> numpoly.logical_and(const > 1, const < 4)
        array([False, False,  True,  True, False])

    """
    x1 = numpoly.aspolynomial(x1)
    x2 = numpoly.aspolynomial(x2)
    coefficients1 = numpy.any(numpy.asarray(x1.coefficients), 0)
    coefficients2 = numpy.any(numpy.asarray(x2.coefficients), 0)
    where_ = numpy.asarray(where)
    return numpy.logical_and(
        coefficients1, coefficients2, out=out, where=where_, **kwargs)
