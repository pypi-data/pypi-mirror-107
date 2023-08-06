from typing import Optional
from uuid import UUID
from pyfactcast.client.sync import FactStore


fact_store = FactStore()


def serial_of(fact_id: UUID) -> Optional[str]:
    with fact_store as fs:
        return fs.serial_of(fact_id=fact_id)
