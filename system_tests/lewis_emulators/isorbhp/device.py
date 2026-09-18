from collections import OrderedDict

from lewis.devices import StateMachineDevice

from .states import DefaultState


class SimulatedIsorbhp(StateMachineDevice):
    def _initialize_data(self) -> None:
        """
        Initialize the device's attributes.
        """
        self.connected = True
        self.is_paused = False
        self.equilibration_started = "01/05/1707 00:00:00"

        self.manifold_pressure = 0
        self.manifold_pressure_ts = "01/05/1707 00:00:00"
        self.cell1_pressure = 0
        self.cell1_pressure_ts = "01/05/1707 00:00:00"
        self.cell2_pressure = 0
        self.cell2_pressure_ts = "01/05/1707 00:00:00"

    def _get_state_handlers(self) -> dict:
        return {
            "default": DefaultState(),
        }

    def _get_initial_state(self) -> str:
        return "default"

    def _get_transition_handlers(self) -> OrderedDict:
        return OrderedDict([])
