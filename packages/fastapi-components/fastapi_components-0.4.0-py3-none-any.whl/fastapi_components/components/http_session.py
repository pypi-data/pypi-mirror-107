from typing import Optional

import aiohttp
from fastapi_components.components.base import BaseComponent
from fastapi_components.state import State


class AIOHTTPSessionComponent(BaseComponent):
    session: Optional[aiohttp.ClientSession]

    async def startup(self, state: State) -> State:
        state.session = aiohttp.ClientSession()
        return state

    async def shutdown(self) -> None:
        if self.session:
            await self.session.close()
