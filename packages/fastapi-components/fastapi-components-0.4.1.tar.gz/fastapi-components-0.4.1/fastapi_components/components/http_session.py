from typing import Optional

import aiohttp

from fastapi_components.components.base import BaseComponent
from fastapi_components.state import State


class AIOHTTPSessionComponent(BaseComponent):
    session: Optional[aiohttp.ClientSession] = None

    async def startup(self, state: State) -> State:
        self.session = aiohttp.ClientSession()
        state.session = self.session
        return state

    async def shutdown(self) -> None:
        if self.session:
            await self.session.close()
