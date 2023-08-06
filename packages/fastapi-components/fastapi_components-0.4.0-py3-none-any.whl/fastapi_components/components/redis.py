from typing import Optional

import aioredis
from fastapi_components.components.base import BaseComponent
from fastapi_components.state import State


class AIORedisComponent(BaseComponent):
    redis: Optional[aioredis.ConnectionsPool]

    async def startup(self, state: State) -> State:
        self.redis = await aioredis.create_redis_pool(state.settings.redis_dsn)
        state.redis = self.redis

        return state

    async def shutdown(self) -> None:
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()
