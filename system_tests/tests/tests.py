import unittest

from utils.channel_access import ChannelAccess  # pyright: ignore
from utils.ioc_launcher import get_default_ioc_dir  # pyright: ignore
from utils.test_modes import TestModes  # pyright: ignore
from utils.testing import get_running_lewis_and_ioc  # pyright: ignore

DEVICE_PREFIX = "ISORBHP_01"


IOCS = [
    {
        "name": DEVICE_PREFIX,
        "directory": get_default_ioc_dir("ISORBHP"),
        "emulator": "isorbhp",
    },
]


TEST_MODES = [TestModes.DEVSIM]


class IsorbhpTests(unittest.TestCase):
    """
    Tests for the ISORBHP IOC.
    """

    def setUp(self):
        self._lewis, self._ioc = get_running_lewis_and_ioc("isorbhp", DEVICE_PREFIX)
        self.ca = ChannelAccess(device_prefix=DEVICE_PREFIX, default_timeout=30)

    def test_pause_resume_analysis(self):
        self._lewis.backdoor_set_on_device("is_paused", True)
        self.ca.assert_that_pv_is("PAUSED", "Analysis Paused")
        self._lewis.backdoor_set_on_device("is_paused", False)
        self.ca.assert_that_pv_is("PAUSED", "Analysis Running")

    def test_equilibration_started(self):
        self._lewis.backdoor_set_on_device("equilibration_started", "1970/01/01 12:34:56")
        self.ca.assert_that_pv_is("EQ_STARTED", "1970/01/01 12:34:56")
        self._lewis.backdoor_set_on_device("equilibration_started", "3000/12/12 23:59:59")
        self.ca.assert_that_pv_is("EQ_STARTED", "3000/12/12 23:59:59")

    def test_manifold_pressure(self):
        self._lewis.backdoor_set_on_device("manifold_pressure", 123.456)
        self._lewis.backdoor_set_on_device("manifold_pressure_ts", "1970/01/01 12:34:56")

        self.ca.assert_that_pv_is_number("PRESSURE:MANIFOLD", 123.456, tolerance=0.001)
        self.ca.assert_that_pv_is("PRESSURE:MANIFOLD:TS", "1970/01/01 12:34:56")

    def test_cell1_pressure(self):
        self._lewis.backdoor_set_on_device("cell1_pressure", 123.456)
        self._lewis.backdoor_set_on_device("cell1_pressure_ts", "1970/01/01 12:34:56")

        self.ca.assert_that_pv_is_number("PRESSURE:CELL1", 123.456, tolerance=0.001)
        self.ca.assert_that_pv_is("PRESSURE:CELL1:TS", "1970/01/01 12:34:56")

    def test_cell2_pressure(self):
        self._lewis.backdoor_set_on_device("cell2_pressure", 123.456)
        self._lewis.backdoor_set_on_device("cell2_pressure_ts", "1970/01/01 12:34:56")

        self.ca.assert_that_pv_is_number("PRESSURE:CELL2", 123.456, tolerance=0.001)
        self.ca.assert_that_pv_is("PRESSURE:CELL2:TS", "1970/01/01 12:34:56")
