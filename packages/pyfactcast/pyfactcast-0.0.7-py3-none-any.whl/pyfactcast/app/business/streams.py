from itertools import zip_longest
import re
from uuid import UUID
from pyfactcast.client.entities import Fact, VersionedType
from typing import Iterable, List
from pyfactcast.client.sync import FactStore


fact_store = FactStore()


def filter_types(*, fs: FactStore, namespace: str, it: Iterable[str]) -> Iterable[str]:
    if not it:
        return it

    types_for_namespace = fs.enumerate_types(namespace=namespace)
    res = set()

    # TODO: Make the regex stuff beautiful
    regexes = [re.compile(elem) for elem in it]
    for regexp in regexes:
        res.update(list(filter(regexp.fullmatch, types_for_namespace)))

    return res


def subscribe(
    namespace: str,
    follow: bool,
    from_now: bool = False,
    after_fact: UUID = None,
    fact_types: List[str] = [],
    type_versions: List[int] = [],
) -> Iterable[Fact]:

    if len(type_versions) > len(fact_types):
        raise ValueError(
            (
                "More versions than event types given."
                "Please provide the same number of types and versions or more types than versions."
            )
        )

    if type_versions:
        lookup_types = [
            VersionedType(type=type_name, version=version)
            for type_name, version in zip_longest(
                fact_types, type_versions, fillvalue=0
            )
        ]

    with fact_store as fs:

        if not type_versions:
            resolved_types = filter_types(fs=fs, namespace=namespace, it=fact_types)
            lookup_types = [
                VersionedType(type=type_name, version=version)
                for type_name, version in zip_longest(
                    resolved_types, type_versions, fillvalue=0
                )
            ]

        return fs.subscribe(
            namespace=namespace,
            continuous=follow,
            from_now=from_now,
            after_fact=after_fact,
            fact_types=lookup_types,
        )
