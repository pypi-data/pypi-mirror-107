"""Electro-Search Algorithm.
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


class ESA(Optimizer):
    """An ESA class, inherited from Optimizer.

    This is the designed class to define ES-related
    variables and methods.

    References:
        A. Tabari and A. Ahmad. A new optimization method: Electro-Search algorithm.
        Computers & Chemical Engineering (2017).

    """

    def __init__(self, params=None):
        """Initialization method.

        Args:
            params (dict): Contains key-value parameters to the meta-heuristics.

        """

        logger.info('Overriding class: Optimizer -> ESA.')

        # Overrides its parent class with the receiving params
        super(ESA, self).__init__()

        # Builds the class
        self.build(params)

        logger.info('Class overrided.')
