import abc

from fastapi_components.state import State
class BaseComponent(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def startup(self, state: State) -> State:
        pass

    @abc.abstractmethod
    async def shutdown(self) -> None:
        pass
