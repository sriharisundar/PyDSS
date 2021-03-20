
from collections import deque
from datetime import datetime, timedelta
import logging

import numpy as np
import opendssdirect as dss
import pandas as pd

from PyDSS.common import DATE_FORMAT


logger = logging.getLogger(__name__)


class CircularBufferHelper:
    def __init__(self, window_size):
        self._buf = deque(maxlen=window_size)
        self._window_size = window_size

    def __len__(self):
        return len(self._buf)

    def append(self, val):
        self._buf.append(val)

    def average(self):
        assert self._buf
        if isinstance(self._buf[0], list):
            return pd.DataFrame(self._buf).rolling(self._window_size).mean().values
        if len(self._buf) < self._window_size:
            return np.NaN
        return sum(self._buf) / len(self._buf)


class TimerStats:
    """Tracks timer stats."""
    def __init__(self, label):
        self._label = label
        self._count = 0
        self._max = 0.0
        self._min = None
        self._avg = 0.0
        self._total = 0.0

    def get_stats(self):
        """Get the current stats summary.

        Returns
        -------
        dict

        """
        avg = 0 if self._count == 0 else self._total / self._count
        return {
            "min": self._min,
            "max": self._max,
            "total": self._total,
            "avg": avg,
            "count": self._count,
        }

    def log_stats(self):
        """Log a summary of the stats."""
        if self._count == 0:
            logger.info("No stats have been recorded for %s.", self._label)
            return

        x = self.get_stats()
        text = "total={:.3f}s avg={:.3f}ms max={:.3f}ms min={:.3f}ms count={}".format(
            x["total"], x["avg"] * 1000, x["max"] * 1000, x["min"] * 1000, x["count"]
        )
        logger.info("TimerStats summary: %s: %s", self._label, text)

    def update(self, duration):
        """Update the stats with a new timing."""
        self._count += 1
        self._total += duration
        if duration > self._max:
            self._max = duration
        if self._min is None or duration < self._min:
            self._min = duration


def get_start_time(settings):
    """Return the start time of the simulation.

    Parameters
    ----------
    settings : dict
        settings from project simulation.toml

    Returns
    -------
    datetime

    """
    return datetime.strptime(settings['Project']["Start time"], DATE_FORMAT)


def get_simulation_resolution(settings):
    """Return the simulation of the resolution

    Parameters
    ----------
    settings : dict
        settings from project simulation.toml

    Returns
    -------
    datetime

    """
    return timedelta(seconds=settings["Project"]["Step resolution (sec)"])


def create_time_range_from_settings(settings):
    """Return the start time, step time, and end time from the settings.

    Parameters
    ----------
    settings : dict
        settings from project simulation.toml

    Returns
    -------
    tuple
        (start, end, step)

    """
    start_time = get_start_time(settings)
    end_time = start_time + timedelta(minutes=settings["Project"]["Simulation duration (min)"])
    step_time = get_simulation_resolution(settings)
    return start_time, end_time, step_time


def create_datetime_index_from_settings(settings):
    """Return time indices created from the simulation settings.

    Parameters
    ----------
    settings : dict
        settings from project simulation.toml

    Returns
    -------
    pd.DatetimeIndex

    """
    start_time, end_time, step_time = create_time_range_from_settings(settings)
    data = []
    cur_time = start_time
    while cur_time < end_time:
        data.append(cur_time)
        cur_time += step_time

    return pd.DatetimeIndex(data)


def create_loadshape_pmult_dataframe(settings):
    """Return a loadshape dataframe representing all available data.
    This assumes that a loadshape has been selected in OpenDSS.

    Parameters
    ----------
    settings : dict
        settings from project simulation.toml

    Returns
    -------
    pd.DatetimeIndex

    """
    start_time = datetime.strptime(settings['Project']['Loadshape start time'], DATE_FORMAT)
    data = dss.LoadShape.PMult()
    interval = timedelta(seconds=dss.LoadShape.SInterval())
    npts = dss.LoadShape.Npts()

    indices = []
    cur_time = start_time
    for _ in range(npts):
        indices.append(cur_time)
        cur_time += interval

    return pd.DataFrame(data, index=pd.DatetimeIndex(indices))


def create_loadshape_pmult_dataframe_for_simulation(settings):
    """Return a loadshape pmult dataframe that only contains time points used
    by the simulation.
    This assumes that a loadshape has been selected in OpenDSS.

    Parameters
    ----------
    settings : dict
        settings from project simulation.toml

    Returns
    -------
    pd.DataFrame

    """
    df = create_loadshape_pmult_dataframe(settings)
    simulation_index = create_datetime_index_from_settings(settings)
    return df.loc[simulation_index]
