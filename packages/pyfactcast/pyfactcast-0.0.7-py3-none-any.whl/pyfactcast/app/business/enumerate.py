from typing import List

from pyfactcast.client.sync import FactStore


fact_store = FactStore()


def namespaces() -> List[str]:
    with fact_store as fs:
        return fs.enumerate_namespaces()


def types(namespace: str) -> List[str]:
    with fact_store as fs:
        return fs.enumerate_types(namespace)
