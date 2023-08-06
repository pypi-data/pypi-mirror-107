from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from time import sleep
from types import TracebackType
from typing import Dict, Tuple, Optional

from docker import from_env as docker_client, DockerClient
from docker.models import containers
from docker.errors import NotFound, ImageNotFound

from .config import Px4FirmwareConfig, Px4StackConfig
from .context import Px4StackContext


def _separate_image_name(image_name: str) -> Tuple[str, Optional[str]]:
    parts = image_name.split(":")

    if len(parts) == 1:
        return parts[0], None
    elif len(parts) == 2:
        return parts[0], parts[1]
    else:
        raise ValueError("Image name cannot be separated")


def _ensure_image(client: DockerClient, image_name: str) -> None:
    try:
        client.images.get(image_name)
    except ImageNotFound:
        name, tag = _separate_image_name(image_name)
        client.images.pull(name, tag)


def _start_stack(*stack: containers.Container) -> None:
    for container in stack:
        try:
            container.start()
        except NotFound:
            raise RuntimeError(f"Could not find container {container.name} to start")


def _stop_stack(*stack: containers.Container) -> None:
    for container in stack:
        try:
            container.kill()
        except NotFound:
            raise RuntimeError(f"Could not find container {container.name} to stop")


def _stack_ready(*stack: containers.Container) -> bool:
    for container in stack:
        try:
            container.reload()
        except NotFound:
            raise RuntimeError(f"Could not find container {container.name} to reload")

    return all(container.status == "running" for container in stack)


class Px4Stack:
    def __init__(self, prefix: str, config: Px4StackConfig):
        client = docker_client()
        log_dest = TemporaryDirectory(prefix=f"{prefix}_", suffix="_logs")
        network_name = f"{prefix}_net"
        px4_name = f"{prefix}_px4"
        px4_volumes: Dict[str, containers.VolumeConfig] = {
            log_dest.name: {"bind": str(config.px4.log_path), "mode": "rw"}
        }

        if config.px4.firmware:
            source_path = config.px4.firmware.source_path.resolve()
            px4_volumes[str(source_path)] = {
                "bind": str(config.px4.firmware.mount_path),
                "mode": "rw",
            }

        _ensure_image(client, config.px4.image)
        _ensure_image(client, config.mavsdk.image)

        if config.px4.firmware is not None:
            build_path = config.px4.firmware.source_path / "build"
            if not build_path.is_dir():
                raise ValueError("firmware must be built before stack can be brought online")

        self.network = client.networks.create(network_name, driver="bridge")

        self.px4_container = client.containers.create(
            config.px4.image,
            command=config.px4.command,
            network=network_name,
            volumes=px4_volumes,
            environment={
                "PX4_SIM_SPEED_FACTOR": str(config.px4.speed),
                "PX4_HOME_LAT": str(config.px4.initial_position[0]),
                "PX4_HOME_LON": str(config.px4.initial_position[1]),
            },
            name=px4_name,
            tty=True,
            auto_remove=True,
            stdin_open=True,
        )

        self.mavsdk_port = f"{config.mavsdk.port}/tcp"

        self.mavsdk_container = client.containers.create(
            config.mavsdk.image,
            command=config.mavsdk.command,
            network=network_name,
            links={px4_name: "px4"},
            ports={self.mavsdk_port: None},
            name=f"{prefix}_mavsdk",
            tty=True,
            auto_remove=True,
        )
        self.log_dest = log_dest

    def __enter__(self) -> Px4StackContext:
        _start_stack(self.px4_container, self.mavsdk_container)

        while not _stack_ready(self.px4_container, self.mavsdk_container):
            sleep(0.05)

        return Px4StackContext(
            self.network,
            self.px4_container,
            self.mavsdk_container,
            self.mavsdk_port,
            Path(self.log_dest.name),
        )

    def __exit__(self, ex_type: Exception, value: object, traceback: TracebackType) -> None:
        _stop_stack(self.mavsdk_container, self.px4_container)
        self.network.remove()
        self.log_dest.cleanup()
