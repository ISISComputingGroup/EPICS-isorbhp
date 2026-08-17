import logging
import typing

from lewis.adapters.stream import StreamInterface
from lewis.core.logging import has_log
from lewis.utils.command_builder import CmdBuilder
from lewis.utils.replies import conditional_reply

if typing.TYPE_CHECKING:
    from ..device import SimulatedIsorbhp

if_connected = conditional_reply("connected")


@has_log
class IsorbhpStreamInterface(StreamInterface):
    in_terminator = "\r\n\r\n"
    out_terminator = ""

    def __init__(self) -> None:
        super().__init__()
        self.log: logging.Logger
        self.device: SimulatedIsorbhp

        self.commands = {
            CmdBuilder(self.is_paused)
            .escape("GET /is_paused HTTP/1.1\r\n")
            .regex(r"[\w\W]*")
            .eos()
            .build(),
            CmdBuilder(self.equilibration_started)
            .escape("GET /equilibration_started HTTP/1.1\r\n")
            .regex(r"[\w\W]*")
            .eos()
            .build(),
            CmdBuilder(self.manifold_pressure)
            .escape("GET /manifold_pressure HTTP/1.1\r\n")
            .regex(r"[\w\W]*")
            .eos()
            .build(),
            CmdBuilder(self.cell1_pressure)
            .escape("GET /cell1_pressure HTTP/1.1\r\n")
            .regex(r"[\w\W]*")
            .eos()
            .build(),
            CmdBuilder(self.cell2_pressure)
            .escape("GET /cell2_pressure HTTP/1.1\r\n")
            .regex(r"[\w\W]*")
            .eos()
            .build(),
        }

    def handle_error(self, request: str, error: str) -> None:
        """
        If command is not recognised print and error

        Args:
            request: requested string
            error: problem

        """
        self.log.error("An error occurred at request " + repr(request) + ": " + repr(error))

    @if_connected
    def is_paused(self) -> str:
        return "HTTP/1.1 200 OK\r\ncontent-type: application/json\r\n\r\n" + (
            "true" if self.device.is_paused else "false"
        )

    @if_connected
    def equilibration_started(self) -> str:
        return (
            "HTTP/1.1 200 OK\r\n"
            "content-type: application/json\r\n\r\n" + f'"{self.device.equilibration_started}"'
        )

    @if_connected
    def manifold_pressure(self) -> str:
        return (
            "HTTP/1.1 200 OK\r\n"
            f"content-type: application/json\r\n\r\n"
            f'[{self.device.manifold_pressure},"{self.device.manifold_pressure_ts}"]'
        )

    @if_connected
    def cell1_pressure(self) -> str:
        return (
            "HTTP/1.1 200 OK\r\n"
            f"content-type: application/json\r\n\r\n"
            f'[{self.device.cell1_pressure},"{self.device.cell1_pressure_ts}"]'
        )

    @if_connected
    def cell2_pressure(self) -> str:
        return (
            "HTTP/1.1 200 OK\r\n"
            f"content-type: application/json\r\n\r\n"
            f'[{self.device.cell2_pressure},"{self.device.cell2_pressure_ts}"]'
        )
