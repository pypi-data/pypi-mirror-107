import json
import logging
import grpc
import struct
from types import TracebackType
from typing import Dict, Iterable, List, Optional, Type, Union
from json import dumps
from uuid import UUID

from pyfactcast.grpc.generated.FactStore_pb2_grpc import RemoteFactStoreStub
from pyfactcast.grpc.generated.FactStore_pb2 import (
    MSG_Empty,
    MSG_Fact,
    MSG_Facts,
    MSG_String,
    MSG_SubscriptionRequest,
    MSG_Notification,
    MSG_UUID,
)

from pyfactcast.client.auth.basic import BasicAuth
from pyfactcast.client.config import (
    ClientConfiguration,
    get_client_configuration,
    log_level,
)
from pyfactcast.client.entities import Fact, VersionedType

log = logging.getLogger()
log.setLevel(log_level)


def get_synchronous_grpc_client(
    client_configuration: Optional[ClientConfiguration] = None,
) -> RemoteFactStoreStub:

    if not client_configuration:
        client_configuration = get_client_configuration()

    if client_configuration.insecure:
        return RemoteFactStoreStub(grpc.insecure_channel(client_configuration.server))

    options = None
    if client_configuration.ssl_target_override:
        options = (
            (
                "grpc.ssl_target_name_override",
                client_configuration.ssl_target_override,
            ),
        )

    root_cert = None
    if client_configuration.root_cert_path:
        with open(client_configuration.root_cert_path) as f:
            root_cert = f.read().encode("UTF-8")

    channel_credentials = grpc.ssl_channel_credentials(root_certificates=root_cert)

    call_credentials = _construct_call_credentials(client_configuration)

    if call_credentials:
        grpc_credentials = grpc.composite_channel_credentials(
            channel_credentials, call_credentials
        )
    else:
        grpc_credentials = channel_credentials

    channel = grpc.secure_channel(
        target=client_configuration.server,
        credentials=grpc_credentials,
        options=options,
    )

    return RemoteFactStoreStub(channel)


def _construct_call_credentials(
    client_configuration: ClientConfiguration,
) -> Optional[grpc.CallCredentials]:

    if client_configuration.credentials:  # 3.8 Walrus
        call_credentials = grpc.metadata_call_credentials(
            BasicAuth(
                client_configuration.credentials.username,
                client_configuration.credentials.password,
            )
        )
        return call_credentials
    return None


def _fact_filter(msg: MSG_Notification) -> bool:
    if msg.type == msg.Fact:
        return True
    elif msg.type == msg.Catchup:
        log.info("Caught up!")
    elif msg.type == msg.facts:
        log.error("Multiple facts per Notification not implemented.")
    elif msg.type == msg.Complete:
        log.debug("Received stream complete.")
    else:
        log.debug(f"Received Notification of type: {msg.type}")
    return False


class FactStore:
    def __init__(self, client: Optional[RemoteFactStoreStub] = None) -> None:
        self._client = client

    def __enter__(self) -> "FactStore":
        if not self._client:
            self.client = get_synchronous_grpc_client()
        else:
            self.client = self._client
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        # TODO: Implement proper channel termination
        pass

    def enumerate_namespaces(self) -> List[str]:
        res: List[str] = self.client.enumerateNamespaces(MSG_Empty()).embeddedString

        return res

    def enumerate_types(self, namespace: str) -> List[str]:
        message = MSG_String()
        message.embeddedString = namespace
        res: List[str] = self.client.enumerateTypes(message).embeddedString

        return res

    def subscribe(
        self,
        *,
        namespace: str,
        continuous: bool = False,
        from_now: bool = False,
        after_fact: UUID = None,
        fact_types: Iterable[VersionedType] = [],
    ) -> Iterable[Fact]:

        specs: List[Dict[str, Union[str, int]]] = [{"ns": namespace}]
        if fact_types:
            specs = [
                {"ns": namespace, "type": fact_type.type, "version": fact_type.version}
                for fact_type in fact_types
            ]

        subscription_request_body = {
            "specs": specs,
            "continuous": continuous,
        }

        if from_now:
            subscription_request_body["ephemeral"] = True
            subscription_request_body["continuous"] = True

        if after_fact:
            subscription_request_body["startingAfter"] = str(after_fact)

        msg = MSG_SubscriptionRequest(json=dumps(subscription_request_body))
        res = self.client.subscribe(msg)

        return map(Fact.from_msg, filter(_fact_filter, res))

    def serial_of(self, *, fact_id: UUID) -> Optional[str]:
        msb, lsb = struct.unpack(">qq", fact_id.bytes)
        msg = MSG_UUID()
        msg.lsb = lsb
        msg.msb = msb
        res = self.client.serialOf(msg)

        if res.present:
            return str(res.serial)
        return None

    def publish(self, *, fact: Fact, conditional: bool = False) -> None:
        if conditional:
            raise NotImplementedError()
        else:
            fact_msg = MSG_Fact(
                header=fact.header.json(), payload=json.dumps(fact.payload)
            )
            msg = MSG_Facts(fact=[fact_msg])
            self.client.publish(msg)
