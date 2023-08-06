from typing import List, Optional

import aiokafka

from fastapi_components.components.base import BaseComponent
from fastapi_components.state import State


class KafkaProducerComponent(BaseComponent):
    required_settings = {"kafka_servers": (List[str], ...)}

    producer: Optional[aiokafka.AIOKafkaProducer]

    async def startup(self, state: State) -> State:
        self.producer = aiokafka.AIOKafkaProducer(bootstrap_servers=state.settings.kafka_servers)

        await self.producer.start()
        state.producer = self.producer
        return state

    async def shutdown(self) -> None:
        if self.producer:
            await self.producer.stop()
