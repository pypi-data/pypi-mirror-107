from dataclasses import dataclass
from typing import Optional

import logging
from os import environ as env


log_level = getattr(
    logging, env.get("FACTCAST_LOG_LEVEL", "WARNING").upper(), 30
)  # Setting a default here is pretty defensive. Anyhow nothing lost by doing it


@dataclass
class Credentials:
    username: str
    password: str

    def __post_init__(self):
        if self.username and not self.password:
            raise ValueError(
                "Username was provided without password. Please provide a non empty password."
            )
        if self.password and not self.username:
            raise ValueError(
                "Password was provided without a username. Please provide a non empty username."
            )
        if not self.username and not self.password:
            raise ValueError(
                "Both username and password are empty. Do not instantiate Credentials like this."
            )


@dataclass
class ClientConfiguration:
    server: str
    root_cert_path: Optional[str] = None
    ssl_target_override: Optional[str] = None
    credentials: Optional[Credentials] = None
    insecure: bool = False

    def __post_init__(self):
        if not self.server:
            raise ValueError("Server connection string missing.")


def get_client_configuration() -> ClientConfiguration:
    username = env.get("GRPC_USER", "")
    password = env.get("GRPC_PASSWORD", "")
    credentials = None

    if username or password:
        credentials = Credentials(username, password)

    return ClientConfiguration(
        server=env.get("GRPC_SERVER", ""),
        credentials=credentials,
        root_cert_path=env.get("GRPC_ROOT_CERT_PATH"),
        ssl_target_override=env.get("GRPC_CN_OVERWRITE"),
        insecure=bool(env.get("GRPC_INSECURE", False)),
    )
