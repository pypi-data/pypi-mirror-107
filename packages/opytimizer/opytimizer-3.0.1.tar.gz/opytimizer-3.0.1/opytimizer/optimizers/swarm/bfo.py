"""Bacterial Foraging Optimization.
"""

import copy

import numpy as np
from tqdm import tqdm

import opytimizer.math.random as r
import opytimizer.utils.constant as c
import opytimizer.utils.exception as e
import opytimizer.utils.history as h
import opytimizer.utils.logging as l
from opytimizer.core import Optimizer

logger = l.get_logger(__name__)


class BFO(Optimizer):
    """A BFO class, inherited from Optimizer.

    This is the designed class to define BFO-related
    variables and methods.

    References:
        S. Das et al. Bacterial Foraging Optimization Algorithm: Theoretical Foundations, Analysis, and Applications.
        Foundations of Computational Intelligence (2009).

    """

    def __init__(self, params=None):
        """Initialization method.

        Args:
            params (dict): Contains key-value parameters to the meta-heuristics.

        """

        logger.info('Overriding class: Optimizer -> BFO.')

        # Overrides its parent class with the receiving params
        super(BFO, self).__init__()

        # Builds the class
        self.build(params)

        logger.info('Class overrided.')
