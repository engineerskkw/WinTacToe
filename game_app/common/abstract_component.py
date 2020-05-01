from abc import ABC, abstractmethod


class AbstractComponent(ABC):
    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def loop(self):
        pass
