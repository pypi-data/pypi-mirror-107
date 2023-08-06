# pylint: disable=line-too-long
# From PyTorch:
#
# Copyright (c) 2016-     Facebook, Inc            (Adam Paszke)
# Copyright (c) 2014-     Facebook, Inc            (Soumith Chintala)
# Copyright (c) 2011-2014 Idiap Research Institute (Ronan Collobert)
# Copyright (c) 2012-2014 Deepmind Technologies    (Koray Kavukcuoglu)
# Copyright (c) 2011-2012 NEC Laboratories America (Koray Kavukcuoglu)
# Copyright (c) 2011-2013 NYU                      (Clement Farabet)
# Copyright (c) 2006-2010 NEC Laboratories America (Ronan Collobert, Leon Bottou, Iain Melvin, Jason Weston)
# Copyright (c) 2006      Idiap Research Institute (Samy Bengio)
# Copyright (c) 2001-2004 Idiap Research Institute (Ronan Collobert, Samy Bengio, Johnny Mariethoz)
#
# From Caffe2:
#
# Copyright (c) 2016-present, Facebook Inc. All rights reserved.
#
# All contributions by Facebook:
# Copyright (c) 2016 Facebook Inc.
#
# All contributions by Google:
# Copyright (c) 2015 Google Inc.
# All rights reserved.
#
# All contributions by Yangqing Jia:
# Copyright (c) 2015 Yangqing Jia
# All rights reserved.
#
# All contributions by Kakao Brain:
# Copyright 2019-2020 Kakao Brain
#
# All contributions from Caffe:
# Copyright(c) 2013, 2014, 2015, the respective contributors
# All rights reserved.
#
# All other contributions:
# Copyright(c) 2015, 2016 the respective contributors
# All rights reserved.
#
# Caffe2 uses a copyright model similar to Caffe: each contributor holds
# copyright over their contributions to Caffe2. The project versioning records
# all such contribution and copyright details. If a contributor wants to further
# mark their specific copyright on a particular contribution, they should
# indicate their copyright solely in the commit message of the change when it is
# committed.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the names of Facebook, Deepmind Technologies, NYU, NEC Laboratories America
#    and IDIAP Research Institute nor the names of its contributors may be
#    used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""
Fork of torch.distributions.tranforms that supports being pickled.
"""
import math
import numbers

import torch
import torch.nn.functional as F
from torch.distributions import constraints
from torch.distributions.utils import _sum_rightmost, broadcast_all, lazy_property
from torch.nn.functional import pad


# pylint: disable=abstract-method,protected-access
class Transform:
    """
    Abstract class for invertable transformations with computable log
    det jacobians. They are primarily used in
    :class:`torch.distributions.TransformedDistribution`.

    Caching is useful for tranforms whose inverses are either expensive or
    numerically unstable. Note that care must be taken with memoized values
    since the autograd graph may be reversed. For example while the following
    works with or without caching::

        y = t(x)
        t.log_abs_det_jacobian(x, y).backward()  # x will receive gradients.

    However the following will error when caching due to dependency reversal::

        y = t(x)
        z = t.inv(y)
        grad(z.sum(), [y])  # error because z is x

    Derived classes should implement one or both of :meth:`_call` or
    :meth:`_inverse`. Derived classes that set `bijective=True` should also
    implement :meth:`log_abs_det_jacobian`.

    Args:
        cache_size (int): Size of cache. If zero, no caching is done. If one,
            the latest single value is cached. Only 0 and 1 are supported.

    Attributes:
        domain (:class:`constraints.Constraint`):
            The constraint representing valid inputs to this transform.
        codomain (:class:`constraints.Constraint`):
            The constraint representing valid outputs to this transform
            which are inputs to the inverse transform.
        bijective (bool): Whether this transform is bijective. A transform
            ``t`` is bijective iff ``t.inv(t(x)) == x`` and
            ``t(t.inv(y)) == y`` for every ``x`` in the domain and ``y`` in
            the codomain. Transforms that are not bijective should at least
            maintain the weaker pseudoinverse properties
            ``t(t.inv(t(x)) == t(x)`` and ``t.inv(t(t.inv(y))) == t.inv(y)``.
        sign (int or Tensor): For bijective univariate transforms, this
            should be +1 or -1 depending on whether transform is monotone
            increasing or decreasing.
        event_dim (int): Number of dimensions that are correlated together in
            the transform ``event_shape``. This should be 0 for pointwise
            transforms, 1 for transforms that act jointly on vectors, 2 for
            transforms that act jointly on matrices, etc.
    """

    bijective = False
    event_dim = 0

    def __init__(self, cache_size=0):
        self._cache_size = cache_size
        self._inv = None
        if cache_size == 0:
            pass  # default behavior
        elif cache_size == 1:
            self._cached_x_y = None, None
        else:
            raise ValueError("cache_size must be 0 or 1")
        super(Transform, self).__init__()

    @property
    def inv(self):
        """
        Returns the inverse :class:`Transform` of this transform.
        This should satisfy ``t.inv.inv == t``.
        """
        return _InverseTransform(self)

    @property
    def sign(self):
        """
        Returns the sign of the determinant of the Jacobian, if applicable.
        In general this only makes sense for bijective transforms.
        """
        raise NotImplementedError

    def __eq__(self, other):
        return self._inv == other._inv

    def __call__(self, x):
        """
        Computes the transform `x => y`.
        """
        if self._cache_size == 0:
            return self._call(x)
        x_old, y_old = self._cached_x_y
        if x is x_old:
            return y_old
        y = self._call(x)
        self._cached_x_y = x, y
        return y

    def _inv_call(self, y):
        """
        Inverts the transform `y => x`.
        """
        if self._cache_size == 0:
            return self._inverse(y)
        x_old, y_old = self._cached_x_y
        if y is y_old:
            return x_old
        x = self._inverse(y)
        self._cached_x_y = x, y
        return x

    def _call(self, x):
        """
        Abstract method to compute forward transformation.
        """
        raise NotImplementedError

    def _inverse(self, y):
        """
        Abstract method to compute inverse transformation.
        """
        raise NotImplementedError

    def log_abs_det_jacobian(self, x, y):
        """
        Computes the log det jacobian `log |dy/dx|` given input and output.
        """
        raise NotImplementedError

    def __repr__(self):
        return self.__class__.__name__ + "()"


class _InverseTransform(Transform):
    """
    Inverts a single :class:`Transform`.
    This class is private; please instead use the ``Transform.inv`` property.
    """

    def __init__(self, transform):
        super(_InverseTransform, self).__init__()
        self._inv = transform

    @constraints.dependent_property
    def domain(self):
        """
        The constraint representing valid inputs to this transform.
        """
        return self._inv.codomain

    @constraints.dependent_property
    def codomain(self):
        """
        The constraint representing valid outputs to this transform
        which are inputs to the inverse transform.
        """
        return self._inv.domain

    @property
    def bijective(self):
        """
        Whether this transform is bijective. A transform ``t``
        is bijective if ``t.inv(t(x)) == x`` and ``t(t.inv(y)) == y``
        for every ``x`` in the domain and ``y`` in the codomain.
        Transforms that are not bijective maintains the weaker
        pseudoinverse properties ``t(t.inv(t(x)) == t(x)`` and
        ``t.inv(t(t.inv(y))) == t.inv(y)``.
        """
        return self._inv.bijective

    @property
    def sign(self):

        """
        Returns the sign of the determinant of the Jacobian, if applicable.
        In general this only makes sense for bijective transforms.
        """
        return self._inv.sign

    @property
    def event_dim(self):
        """
        Number of dimensions that are correlated together in the transform
        ``event_shape``.
        """
        return self._inv.event_dim

    @property
    def inv(self):
        """
        Returns the inverse :class:`Transform` of this transform.
        This should satisfy ``t.inv.inv == t``.
        """
        return self._inv

    def __eq__(self, other):
        if not isinstance(other, _InverseTransform):
            return False
        return self._inv == other._inv

    def __call__(self, x):
        return self._inv._inv_call(x)

    def log_abs_det_jacobian(self, x, y):
        """
        Computes the log det jacobian `log |dy/dx|` given input and output.
        """
        return -self._inv.log_abs_det_jacobian(y, x)


class ComposeTransform(Transform):
    """
    Composes multiple transforms in a chain.
    The transforms being composed are responsible for caching.

    Args:
        parts (list of :class:`Transform`): A list of transforms to compose.
    """

    def __init__(self, parts):
        super(ComposeTransform, self).__init__()
        self.parts = parts

    def __eq__(self, other):
        if not isinstance(other, ComposeTransform):
            return False
        return self.parts == other.parts

    @constraints.dependent_property
    def domain(self):
        """
        The constraint representing valid inputs to this transform.
        """
        if not self.parts:
            return constraints.real
        return self.parts[0].domain

    @constraints.dependent_property
    def codomain(self):
        """
        The constraint representing valid outputs to this transform
        which are inputs to the inverse transform.
        """
        if not self.parts:
            return constraints.real
        return self.parts[-1].codomain

    @lazy_property
    def bijective(self):
        """
        Whether this transform is bijective. A transform ``t``
        is bijective if ``t.inv(t(x)) == x`` and ``t(t.inv(y)) == y``
        for every ``x`` in the domain and ``y`` in the codomain.
        Transforms that are not bijective maintains the weaker
        pseudoinverse properties ``t(t.inv(t(x)) == t(x)`` and
        ``t.inv(t(t.inv(y))) == t.inv(y)``.
        """
        return all(p.bijective for p in self.parts)

    #  pylint:disable=invalid-overridden-method
    @lazy_property
    def sign(self):
        """
        Returns the sign of the determinant of the Jacobian, if applicable.
        In general this only makes sense for bijective transforms.
        """
        sign = 1
        for part in self.parts:
            sign = sign * part.sign
        return sign

    @lazy_property
    def event_dim(self):
        """
        Number of dimensions that are correlated together in the transform
        ``event_shape``.
        """
        return max(p.event_dim for p in self.parts) if self.parts else 0

    @property
    def inv(self):
        return ComposeTransform([p.inv for p in reversed(self.parts)])

    def __call__(self, x):
        for part in self.parts:
            x = part(x)
        return x

    def log_abs_det_jacobian(self, x, y):
        """
        Computes the log det jacobian `log |dy/dx|` given input and output.
        """
        if not self.parts:
            return torch.zeros_like(x)
        result = 0
        for part in self.parts[:-1]:
            y_tmp = part(x)
            result = result + _sum_rightmost(
                part.log_abs_det_jacobian(x, y_tmp), self.event_dim - part.event_dim
            )
            x = y_tmp
        part = self.parts[-1]
        result = result + _sum_rightmost(
            part.log_abs_det_jacobian(x, y), self.event_dim - part.event_dim
        )
        return result

    def __repr__(self):
        fmt_string = self.__class__.__name__ + "(\n    "
        fmt_string += ",\n    ".join([p.__repr__() for p in self.parts])
        fmt_string += "\n)"
        return fmt_string


class IdentityTransform(ComposeTransform):
    """
    Composes multiple transforms in a chain.
    The transforms being composed are responsible for caching.
    """

    def __init__(self):
        super().__init__([])


class ExpTransform(Transform):
    r"""
    Transform via the mapping :math:`y = \exp(x)`.
    """
    domain = constraints.real
    codomain = constraints.positive
    bijective = True
    sign = +1

    def __eq__(self, other):
        return isinstance(other, ExpTransform)

    def _call(self, x):
        return x.exp()

    def _inverse(self, y):
        return y.log()

    def log_abs_det_jacobian(self, x, y):
        """
        Computes the log det jacobian `log |dy/dx|` given input and output.
        """
        return x


class PowerTransform(Transform):
    r"""
    Transform via the mapping :math:`y = x^{\text{exponent}}`.
    """
    domain = constraints.positive
    codomain = constraints.positive
    bijective = True
    sign = +1

    def __init__(self, exponent, cache_size=0):
        super(PowerTransform, self).__init__(cache_size=cache_size)
        (self.exponent,) = broadcast_all(exponent)

    def __eq__(self, other):
        if not isinstance(other, PowerTransform):
            return False
        return self.exponent.eq(other.exponent).all().item()

    def _call(self, x):
        return x.pow(self.exponent)

    def _inverse(self, y):
        return y.pow(1 / self.exponent)

    def log_abs_det_jacobian(self, x, y):
        """
        Computes the log det jacobian `log |dy/dx|` given input and output.
        """
        return (self.exponent * y / x).abs().log()


def _clipped_sigmoid(x):
    finfo = torch.finfo(x.dtype)
    return torch.clamp(torch.sigmoid(x), min=finfo.tiny, max=1.0 - finfo.eps)


class SigmoidTransform(Transform):
    r"""
    Transform via the mapping :math:`y = \frac{1}{1 + \exp(-x)}` and
    :math:`x = \text{logit}(y)`.
    """
    domain = constraints.real
    codomain = constraints.unit_interval
    bijective = True
    sign = +1

    def __eq__(self, other):
        return isinstance(other, SigmoidTransform)

    def _call(self, x):
        return _clipped_sigmoid(x)

    def _inverse(self, y):
        finfo = torch.finfo(y.dtype)
        y = y.clamp(min=finfo.tiny, max=1.0 - finfo.eps)
        return y.log() - (-y).log1p()

    def log_abs_det_jacobian(self, x, y):
        """
        Computes the log det jacobian `log |dy/dx|` given input and output.
        """
        return -F.softplus(-x) - F.softplus(x)


class AbsTransform(Transform):
    r"""
    Transform via the mapping :math:`y = |x|`.
    """
    domain = constraints.real
    codomain = constraints.positive

    def __eq__(self, other):
        return isinstance(other, AbsTransform)

    def _call(self, x):
        return x.abs()

    def _inverse(self, y):
        return y


class AffineTransform(Transform):
    r"""
    Transform via the pointwise affine mapping
    :math:`y = \text{loc} + \text{scale} \times x`.

    Args:
        loc (Tensor or float): Location parameter.
        scale (Tensor or float): Scale parameter.
        event_dim (int): Optional size of `event_shape`. This should be zero
            for univariate random variables, 1 for distributions over vectors,
            2 for distributions over matrices, etc.
    """
    domain = constraints.real
    codomain = constraints.real
    bijective = True

    def __init__(self, loc, scale, event_dim=0, cache_size=0):
        super(AffineTransform, self).__init__(cache_size=cache_size)
        self.loc = loc
        self.scale = scale
        self.event_dim = event_dim

    def __eq__(self, other):
        if not isinstance(other, AffineTransform):
            return False

        loc_eq = self.loc == other.loc
        if not isinstance(loc_eq, bool):
            loc_eq = loc_eq.all().item()

        scale_eq = self.scale == other.scale
        if not isinstance(scale_eq, bool):
            scale_eq = scale_eq.all().item()
        return scale_eq and loc_eq

    @property
    def sign(self):
        """
        Returns the sign of the determinant of the Jacobian, if applicable.
        In general this only makes sense for bijective transforms.
        """
        if isinstance(self.scale, numbers.Number):
            return 1 if self.scale > 0 else -1 if self.scale < 0 else 0
        return self.scale.sign()

    def _call(self, x):
        return self.loc + self.scale * x

    def _inverse(self, y):
        return (y - self.loc) / self.scale

    def log_abs_det_jacobian(self, x, y):
        """
        Computes the log det jacobian `log |dy/dx|` given input and output.
        """
        shape = x.shape
        scale = self.scale
        if isinstance(scale, numbers.Number):
            result = torch.full_like(x, math.log(abs(scale)))
        else:
            result = torch.abs(scale).log()
        if self.event_dim:
            result_size = result.size()[: -self.event_dim] + (-1,)
            result = result.view(result_size).sum(-1)
            shape = shape[: -self.event_dim]
        return result.expand(shape)


class SoftmaxTransform(Transform):
    r"""
    Transform from unconstrained space to the simplex via :math:`y = \exp(x)` then
    normalizing.

    This is not bijective and cannot be used for HMC. However this acts mostly
    coordinate-wise (except for the final normalization), and thus is
    appropriate for coordinate-wise optimization algorithms.
    """
    domain = constraints.real
    codomain = constraints.simplex
    event_dim = 1

    def __eq__(self, other):
        return isinstance(other, SoftmaxTransform)

    def _call(self, x):
        logprobs = x
        probs = (logprobs - logprobs.max(-1, True)[0]).exp()
        return probs / probs.sum(-1, True)

    def _inverse(self, y):
        probs = y
        return probs.log()


class StickBreakingTransform(Transform):
    """
    Transform from unconstrained space to the simplex of one additional
    dimension via a stick-breaking process.

    This transform arises as an iterated sigmoid transform in a stick-breaking
    construction of the `Dirichlet` distribution: the first logit is
    transformed via sigmoid to the first probability and the probability of
    everything else, and then the process recurses.

    This is bijective and appropriate for use in HMC; however it mixes
    coordinates together and is less appropriate for optimization.
    """

    domain = constraints.real
    codomain = constraints.simplex
    bijective = True
    event_dim = 1

    def __eq__(self, other):
        return isinstance(other, StickBreakingTransform)

    def _call(self, x):
        offset = x.shape[-1] + 1 - x.new_ones(x.shape[-1]).cumsum(-1)
        temp = _clipped_sigmoid(x - offset.log())
        temp_cumprod = (1 - temp).cumprod(-1)
        y = pad(temp, (0, 1), value=1) * pad(temp_cumprod, (1, 0), value=1)
        return y

    def _inverse(self, y):
        y_crop = y[..., :-1]
        offset = y.shape[-1] - y.new_ones(y_crop.shape[-1]).cumsum(-1)
        sbf = 1 - y_crop.cumsum(-1)
        # we clamp to make sure that sf is positive which sometimes does not
        # happen when y[-1] ~ 0 or y[:-1].sum() ~ 1
        sbf = torch.clamp(sbf, min=torch.finfo(y.dtype).tiny)
        x = y_crop.log() - sbf.log() + offset.log()
        return x

    def log_abs_det_jacobian(self, x, y):
        """
        Computes the log det jacobian `log |dy/dx|` given input and output.
        """
        offset = x.shape[-1] + 1 - x.new_ones(x.shape[-1]).cumsum(-1)
        x = x - offset.log()
        # use the identity 1 - sigmoid(x) = exp(-x) * sigmoid(x)
        det_j = (-x + F.logsigmoid(x) + y[..., :-1].log()).sum(-1)
        return det_j


class LowerCholeskyTransform(Transform):
    """
    Transform from unconstrained matrices to lower-triangular matrices with
    nonnegative diagonal entries.

    This is useful for parameterizing positive definite matrices in terms of
    their Cholesky factorization.
    """

    domain = constraints.real
    codomain = constraints.lower_cholesky
    event_dim = 2

    def __eq__(self, other):
        return isinstance(other, LowerCholeskyTransform)

    def _call(self, x):
        return x.tril(-1) + x.diagonal(dim1=-2, dim2=-1).exp().diag_embed()

    def _inverse(self, y):
        return y.tril(-1) + y.diagonal(dim1=-2, dim2=-1).log().diag_embed()


class CatTransform(Transform):
    """
    Transform functor that applies a sequence of transforms `tseq`
    component-wise to each submatrix at `dim`, of length `lengths[dim]`,
    in a way compatible with :func:`torch.cat`.

    Example::
       x0 = torch.cat([torch.range(1, 10), torch.range(1, 10)], dim=0)
       x = torch.cat([x0, x0], dim=0)
       t0 = CatTransform([ExpTransform(), IdentityTransform()], dim=0, lengths=[10, 10])
       t = CatTransform([t0, t0], dim=0, lengths=[20, 20])
       y = t(x)
    """

    def __init__(self, tseq, dim=0, lengths=None):
        assert all(isinstance(t, Transform) for t in tseq)
        super(CatTransform, self).__init__()
        self.transforms = list(tseq)
        if lengths is None:
            lengths = [1] * len(self.transforms)
        self.lengths = list(lengths)
        assert len(self.lengths) == len(self.transforms)
        self.dim = dim

    @lazy_property
    def length(self):
        """The number of transforms applied"""
        return sum(self.lengths)

    def _call(self, x):
        assert -x.dim() <= self.dim < x.dim()
        assert x.size(self.dim) == self.length
        yslices = []
        start = 0
        for trans, length in zip(self.transforms, self.lengths):
            xslice = x.narrow(self.dim, start, length)
            yslices.append(trans(xslice))
            start = start + length  # avoid += for jit compat
        return torch.cat(yslices, dim=self.dim)

    def _inverse(self, y):
        assert -y.dim() <= self.dim < y.dim()
        assert y.size(self.dim) == self.length
        xslices = []
        start = 0
        for trans, length in zip(self.transforms, self.lengths):
            yslice = y.narrow(self.dim, start, length)
            xslices.append(trans.inv(yslice))
            start = start + length  # avoid += for jit compat
        return torch.cat(xslices, dim=self.dim)

    def log_abs_det_jacobian(self, x, y):
        """
        Computes the log det jacobian `log |dy/dx|` given input and output.
        """
        assert -x.dim() <= self.dim < x.dim()
        assert x.size(self.dim) == self.length
        assert -y.dim() <= self.dim < y.dim()
        assert y.size(self.dim) == self.length
        logdetjacs = []
        start = 0
        for trans, length in zip(self.transforms, self.lengths):
            xslice = x.narrow(self.dim, start, length)
            yslice = y.narrow(self.dim, start, length)
            logdetjacs.append(trans.log_abs_det_jacobian(xslice, yslice))
            start = start + length  # avoid += for jit compat
        return torch.cat(logdetjacs, dim=self.dim)

    @property
    def bijective(self):
        """
        Whether this transform is bijective. A transform ``t``
        is bijective if ``t.inv(t(x)) == x`` and ``t(t.inv(y)) == y``
        for every ``x`` in the domain and ``y`` in the codomain.
        Transforms that are not bijective maintains the weaker
        pseudoinverse properties ``t(t.inv(t(x)) == t(x)`` and
        ``t.inv(t(t.inv(y))) == t.inv(y)``.
        """
        return all(t.bijective for t in self.transforms)

    @constraints.dependent_property
    def domain(self):
        """
        The constraint representing valid inputs to this transform.
        """
        return constraints.cat(
            [t.domain for t in self.transforms], self.dim, self.lengths
        )

    @constraints.dependent_property
    def codomain(self):
        """
        The constraint representing valid outputs to this transform
        which are inputs to the inverse transform.
        """
        return constraints.cat(
            [t.codomain for t in self.transforms], self.dim, self.lengths
        )


class StackTransform(Transform):
    """
    Transform functor that applies a sequence of transforms `tseq`
    component-wise to each submatrix at `dim`
    in a way compatible with :func:`torch.stack`.

    Example::
       x = torch.stack([torch.range(1, 10), torch.range(1, 10)], dim=1)
       t = StackTransform([ExpTransform(), IdentityTransform()], dim=1)
       y = t(x)
    """

    def __init__(self, tseq, dim=0):
        assert all(isinstance(t, Transform) for t in tseq)
        super(StackTransform, self).__init__()
        self.transforms = list(tseq)
        self.dim = dim

    def _slice(self, x):
        return [x.select(self.dim, i) for i in range(x.size(self.dim))]

    def _call(self, x):
        assert -x.dim() <= self.dim < x.dim()
        assert x.size(self.dim) == len(self.transforms)
        yslices = []
        for xslice, trans in zip(self._slice(x), self.transforms):
            yslices.append(trans(xslice))
        return torch.stack(yslices, dim=self.dim)

    def _inverse(self, y):
        assert -y.dim() <= self.dim < y.dim()
        assert y.size(self.dim) == len(self.transforms)
        xslices = []
        for yslice, trans in zip(self._slice(y), self.transforms):
            xslices.append(trans.inv(yslice))
        return torch.stack(xslices, dim=self.dim)

    def log_abs_det_jacobian(self, x, y):
        """
        Computes the log det jacobian `log |dy/dx|` given input and output.
        """
        assert -x.dim() <= self.dim < x.dim()
        assert x.size(self.dim) == len(self.transforms)
        assert -y.dim() <= self.dim < y.dim()
        assert y.size(self.dim) == len(self.transforms)
        logdetjacs = []
        yslices = self._slice(y)
        xslices = self._slice(x)
        for xslice, yslice, trans in zip(xslices, yslices, self.transforms):
            logdetjacs.append(trans.log_abs_det_jacobian(xslice, yslice))
        return torch.stack(logdetjacs, dim=self.dim)

    @property
    def bijective(self):
        """
        Whether this transform is bijective. A transform ``t``
        is bijective if ``t.inv(t(x)) == x`` and ``t(t.inv(y)) == y``
        for every ``x`` in the domain and ``y`` in the codomain.
        Transforms that are not bijective maintains the weaker
        pseudoinverse properties ``t(t.inv(t(x)) == t(x)`` and
        ``t.inv(t(t.inv(y))) == t.inv(y)``.
        """
        return all(t.bijective for t in self.transforms)

    @constraints.dependent_property
    def domain(self):
        """
        The constraint representing valid inputs to this transform.
        """
        return constraints.stack([t.domain for t in self.transforms], self.dim)

    @constraints.dependent_property
    def codomain(self):
        """
        The constraint representing valid outputs to this transform
        which are inputs to the inverse transform.
        """
        return constraints.stack([t.codomain for t in self.transforms], self.dim)


class IndependentTransform(Transform):
    """
    Wrapper around another transform to treat
    ``reinterpreted_batch_ndims``-many extra of the right most dimensions as
    dependent. This has no effect on the forward or backward transforms, but
    does sum out ``reinterpreted_batch_ndims``-many of the rightmost dimensions
    in :meth:`log_abs_det_jacobian`.
    Args:
        base_transform (:class:`Transform`): A base transform.
        reinterpreted_batch_ndims (int): The number of extra rightmost
            dimensions to treat as dependent.
    """

    def __init__(self, base_transform, reinterpreted_batch_ndims, cache_size=0):
        super().__init__(cache_size=cache_size)
        self.base_transform = base_transform
        self.reinterpreted_batch_ndims = reinterpreted_batch_ndims

    def with_cache(self, cache_size=1):
        """
        use cache
        """
        if self._cache_size == cache_size:
            return self
        return IndependentTransform(
            self.base_transform, self.reinterpreted_batch_ndims, cache_size=cache_size
        )

    @constraints.dependent_property(is_discrete=False)
    def domain(self):
        """
        The constraint representing valid inputs to this transform.
        """
        return constraints.independent(
            self.base_transform.domain, self.reinterpreted_batch_ndims
        )

    @constraints.dependent_property(is_discrete=False)
    def codomain(self):
        """
        The constraint representing valid outputs to this transform
        which are inputs to the inverse transform.
        """
        return constraints.independent(
            self.base_transform.codomain, self.reinterpreted_batch_ndims
        )

    @property
    def bijective(self):
        """
        Whether this transform is bijective. A transform ``t``
        is bijective if ``t.inv(t(x)) == x`` and ``t(t.inv(y)) == y``
        for every ``x`` in the domain and ``y`` in the codomain.
        Transforms that are not bijective maintains the weaker
        pseudoinverse properties ``t(t.inv(t(x)) == t(x)`` and
        ``t.inv(t(t.inv(y))) == t.inv(y)``.
        """
        return self.base_transform.bijective

    @property
    def sign(self):
        """
        Returns the sign of the determinant of the Jacobian, if applicable.
        In general this only makes sense for bijective transforms.
        """
        return self.base_transform.sign

    def _call(self, x):
        if x.dim() < self.domain.event_dim:
            raise ValueError("Too few dimensions on input")
        return self.base_transform(x)

    def _inverse(self, y):
        if y.dim() < self.codomain.event_dim:
            raise ValueError("Too few dimensions on input")
        return self.base_transform.inv(y)

    def log_abs_det_jacobian(self, x, y):
        """
        Computes the log det jacobian `log |dy/dx|` given input and output.
        """
        result = self.base_transform.log_abs_det_jacobian(x, y)
        result = _sum_rightmost(result, self.reinterpreted_batch_ndims)
        return result

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.base_transform)}, {self.reinterpreted_batch_ndims})"

    def forward_shape(self, shape):
        """
        The shape in the forward
        """
        return self.base_transform.forward_shape(shape)

    def inverse_shape(self, shape):
        """
        The shape for the inverse
        """
        return self.base_transform.inverse_shape(shape)
