"""
Distributions
=============

Distributions to use with borch.

It basically does some minor modifications to torch.distributions
"""
from torch.distributions import constraints
from borch.distributions.distributions import *
from borch.distributions import constraints_registry, transforms
