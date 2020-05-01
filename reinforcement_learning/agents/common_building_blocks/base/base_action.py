from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseAction(ABC):
    """Class implements action taken by reinforcement learning agent."""

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
