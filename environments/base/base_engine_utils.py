from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class BasePlayer(ABC):
    """Base class representing a player."""


@dataclass(frozen=True)
class BaseWinning(ABC):
    """Base class representing a winning."""
