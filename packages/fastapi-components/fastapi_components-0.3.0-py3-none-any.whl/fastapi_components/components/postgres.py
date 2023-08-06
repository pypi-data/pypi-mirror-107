from typing import Optional

from aiopg.sa import Engine, create_engine
from zvuk_service_lib.components.base import BaseComponent
from zvuk_service_lib.state import State


class AIOPostgresComponent(BaseComponent):
    engine: Optional[Engine]

    async def startup(self, state: State) -> State:
        self.engine = await create_engine(state.settings.postgres_dsn)
        state.db = self.engine
        return state

    async def shutdown(self) -> None:
        if self.engine:
            self.engine.close()
            await self.engine.wait_closed()
