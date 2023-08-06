from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import AnyUrl

from zvuk_service_lib.components.base import BaseComponent
from zvuk_service_lib.state import State


class MongoDsn(AnyUrl):
    allowed_schemes = {"mongodb"}


class MotorComponent(BaseComponent):
    required_settings = {"mongo_dsn": (MongoDsn, ...)}

    mongo: Optional[AsyncIOMotorClient]

    async def startup(self, state: State) -> State:
        self.mongo = AsyncIOMotorClient(state.settings.mongo_dsn)
        state.mongo = self.mongo
        return state

    async def shutdown(self) -> None:
        if self.mongo:
            self.mongo.close()
