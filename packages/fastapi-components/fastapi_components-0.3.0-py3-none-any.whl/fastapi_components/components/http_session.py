from typing import Optional

import aiohttp
from zvuk_service_lib.components.base import BaseComponent
from zvuk_service_lib.state import State


class AIOHTTPSessionComponent(BaseComponent):
    session: Optional[aiohttp.ClientSession]

    async def startup(self, state: State) -> State:
        state.session = aiohttp.ClientSession()
        return state

    async def shutdown(self) -> None:
        if self.session:
            await self.session.close()
