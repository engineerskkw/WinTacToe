from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseState(ABC):
    """Class implements reinforcement learning state of the environment"""

    @abstractmethod
    def flatten(self):
        """
        Get vectorized representation.

        Returns
        -------
        np.array[np.float64]
            Numpy array of floats
        """
        pass

