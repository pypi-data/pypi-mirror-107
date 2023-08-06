"""Module pdp implements a client for making authz requests to a Policy Decision Point (OPA)"""

__version__ = '0.1.0'

from .client import PolicyDecisionPointClient, AuthzException
from .input import PolicyDecisionPointInput
