from ..abstract_component import AbstractComponent


class AbstractMenuComponent(AbstractComponent):
    def __init__(self):
        self._scene = None
        self._logic = None

    def render(self):
        self._scene.render()

    def handle_event(self, event):
        self._logic.handle_event(event)

    def loop(self):
        pass
