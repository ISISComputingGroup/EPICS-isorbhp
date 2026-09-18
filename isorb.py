# /// script
# requires-python = ">=3.13,<3.14"
# dependencies = [
#   "fastapi",
#   "pywinauto",
#   "tzdata",
#   "uvicorn",
# ]
# ///
import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from pywinauto import Application

LOG_LOCATION = Path("C://", "QCdata", "iSorbHP Data", "log")
"""Location at which the iSorb system stores log files"""

LOG_FILE_MARKER: str = '"Register archive of iSorbHPwin messages"'
"""Marker for the start of a log file (files that do not start with this prefix will be ignored)."""

WAITING_FOR_EQUILIBRIUM_MARKER = "Waiting for thermic equilibrium on Manifold"

LOG_FILE_POLLING_PERIOD_S = 5
"""
How frequently, in seconds, to poll the log file for recent entries.
"""

LOG_FILE_RECENT_S = LOG_FILE_POLLING_PERIOD_S * 3
"""
A log entry is considered recent if the timestamp is within this bound of the current time.
"""

APPLICATION_TITLE_REGEX: str = ".*iSorbHPwin High Pressure Isotherms .*"
"""
Regex to find an open instance of the iSorbHPwin manufacturer software.
"""

MENU_PAUSE_ANALYSIS = "Analysis->Adsorption-Desorption->Pause Analysis"
MENU_RESUME_ANALYSIS = "Analysis->Adsorption-Desorption->Resume Analysis"


logger = logging.getLogger("isorb-hp")
logger.setLevel(logging.DEBUG)
logging.basicConfig()


fastapi_app = FastAPI()


def find_latest_log_file() -> Path:
    files = LOG_LOCATION.glob("*.txt")

    return max(
        [f for f in files if f.read_text(encoding="cp1252").startswith(LOG_FILE_MARKER)],
        key=lambda item: item.stat().st_ctime,
    )


@fastapi_app.get("/equilibration_started")
def equilibration_started() -> str:
    log_file = find_latest_log_file()
    log_file_contents = log_file.read_text(encoding="cp1252")

    most_recent_equilibration_start = "Never"

    for log_line in log_file_contents.splitlines():
        if WAITING_FOR_EQUILIBRIUM_MARKER in log_line:
            most_recent_equilibration_start = log_line[1 : 1 + len("13/08/2026 15:29:40")]

    return most_recent_equilibration_start


@fastapi_app.get("/manifold_pressure")
def manifold_pressure() -> tuple[float, str]:
    log_file = find_latest_log_file()
    log_file_contents = log_file.read_text(encoding="cp1252")

    pressure = -1
    timestamp = "Never"

    for log_line in log_file_contents.splitlines():
        if "Reading pressure with precision on Manifold" in log_line:
            pressure = float(log_line.split(": ")[1].strip('"'))
            timestamp = log_line[1 : 1 + len("13/08/2026 15:29:40")]

    return pressure, timestamp


@fastapi_app.get("/cell1_pressure")
def cell1_pressure() -> tuple[float, str]:
    log_file = find_latest_log_file()
    log_file_contents = log_file.read_text(encoding="cp1252")

    pressure = -1
    timestamp = "Never"

    for log_line in log_file_contents.splitlines():
        if "Reading pressure with precision on Cell 1" in log_line:
            pressure = float(log_line.split(": ")[1].strip('"'))
            timestamp = log_line[1 : 1 + len("13/08/2026 15:29:40")]

    return pressure, timestamp


@fastapi_app.get("/cell2_pressure")
def cell2_pressure() -> tuple[float, str]:
    log_file = find_latest_log_file()
    log_file_contents = log_file.read_text(encoding="cp1252")

    pressure = -1
    timestamp = "Never"

    for log_line in log_file_contents.splitlines():
        if "Reading pressure with precision on Cell 2" in log_line:
            pressure = float(log_line.split(": ")[1].strip('"'))
            timestamp = log_line[1 : 1 + len("13/08/2026 15:29:40")]

    return pressure, timestamp


@fastapi_app.get("/is_paused")
def is_paused() -> bool:
    log_file = find_latest_log_file()
    log_file_contents = log_file.read_text(encoding="cp1252")

    is_paused = False

    for log_line in log_file_contents.splitlines():
        if "Analysis has been paused" in log_line:
            is_paused = True
        elif "Analysis continues" in log_line:
            is_paused = False

    return is_paused


@fastapi_app.post("/pause_analysis")
def pause_analysis() -> None:
    isorbhpwin_application = Application(backend="uia").connect(title_re=APPLICATION_TITLE_REGEX)
    window = isorbhpwin_application.top_window()
    window.menu_select(MENU_PAUSE_ANALYSIS, exact=True)


@fastapi_app.post("/resume_analysis")
def resume_analysis() -> None:
    """Resume an analysis"""
    isorbhpwin_application = Application(backend="uia").connect(title_re=APPLICATION_TITLE_REGEX)
    window = isorbhpwin_application.top_window()
    window.menu_select(MENU_RESUME_ANALYSIS, exact=True)


if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
