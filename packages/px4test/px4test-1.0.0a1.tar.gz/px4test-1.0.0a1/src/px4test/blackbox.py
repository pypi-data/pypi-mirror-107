from __future__ import annotations

from asyncio import run
from csv import writer as csv_writer
from hashlib import md5
from pathlib import Path
from shutil import copy
from typing import Tuple, Callable, Optional

from mavsdk import System
from numpy import float32, ndarray, vstack
from px4ctl import execute
from px4ctl.mission import Mission, Waypoint
from px4ctl.storage import store_mission
from px4stack import Px4Stack, Px4StackConfig
from pyulog import ULog
from staliro.models import (
    blackbox,
    Blackbox,
    StaticParameters,
    SignalTimes,
    SignalValues,
    BlackboxResult,
)

from .config import Px4TestConfig

MissionFactory = Callable[[ndarray, ndarray, ndarray], Mission]


def _default_factory(X: ndarray, *args: ndarray) -> Mission:
    waypoints = tuple(Waypoint(lat=X[i], lon=X[i + 1], alt=5) for i in range(0, X.size, 2))
    geofences = ()

    return Mission(waypoints=waypoints, geofences=geofences)


def _read_flight_log(log_file: Path) -> Tuple[ndarray, ndarray]:
    """Extract drone trajectory information from flight log."""

    with log_file.open("rb") as log:
        parsed_log = ULog(log)
        ground_truth = parsed_log.get_dataset("vehicle_global_position_groundtruth")
        trajectory = vstack((ground_truth.data["lat"], ground_truth.data["lon"]))
        timestamps = ground_truth.data["timestamp"]

        return trajectory.T, timestamps


def _store_flight_trajectory(dest_path: Path, positions: ndarray, times: ndarray) -> None:
    with dest_path.open("w") as file:
        writer = csv_writer(file)
        writer.writerow(("t", "lat", "lon"))

        for i in range(positions.shape[0]):
            writer.writerow((times[i], positions[i][0], positions[i][1]))


def px4_blackbox_factory(
    config: Px4TestConfig,
    stack_config: Px4StackConfig,
    mission_factory: Optional[MissionFactory] = None,
) -> Blackbox:
    """Factory function to create px4 blackbox instances that have access to additional variables."""

    @blackbox()
    def px4_blackbox(X: StaticParameters, T: SignalTimes, U: SignalValues) -> BlackboxResult:
        mission = mission_factory(X, T, U) if mission_factory is not None else _default_factory(X)
        mission_id = md5(X.tobytes()).hexdigest()

        with Px4Stack(mission_id, stack_config) as stack:
            drone = System(mavsdk_server_address="localhost", port=stack.port)
            run(execute(mission, drone, "", verbose=True))
            positions, timestamps = _read_flight_log(stack.flight_log)

            if config.log_dest is not None:
                log_path = config.log_dest / f"{mission_id}.csv"
                _store_flight_trajectory(log_path, positions, timestamps)

            if config.mission_dest is not None:
                store_mission(mission, str(config.mission_dest / f"{mission_id}.json"))

            return positions, timestamps

    return px4_blackbox
