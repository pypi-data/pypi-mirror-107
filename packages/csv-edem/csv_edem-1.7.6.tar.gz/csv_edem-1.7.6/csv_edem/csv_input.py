import logging
import os

import numpy as np

logger = logging.getLogger(__name__)


class CSV_Edem_input:
    def __init__(self, csv_filename: str, lines_to_skip: int = 19):
        logger.info(
            "Creating object CSV_Edem_input with csv file '{}'".format(csv_filename)
        )
        logger.info("Lines to skip: {:d}".format(lines_to_skip))

        self._csv_filename: str = csv_filename
        self._lines_to_skip: int = lines_to_skip

        self.time: np.ndarray = np.array([])
        self.total_col: np.ndarray = np.array([])
        self.avg_col_force_mag: np.ndarray = np.array([])

        self._number_points: int = 0
        self.total_col_mean: float = 0.0
        self.avg_col_force_mag_mean: float = 0.0

    def checkIfFileExists(self) -> bool:
        logger.info("Checking if file '{}' exists".format(self._csv_filename))
        return os.path.isfile(self._csv_filename)

    def getFilename(self) -> str:
        return self._csv_filename

    def extractRawData(self) -> None:
        logger.info("Extracting raw data from {}".format(self._csv_filename))
        self.time, self.total_col, self.avg_col_force_mag = np.genfromtxt(
            self._csv_filename,
            skip_header=self._lines_to_skip,
            unpack=True,
            delimiter=",",
        )
        self._number_points = len(self.time)
        self.total_col = np.asarray(self.total_col, dtype=np.int16)

        logger.info("Number of raw points: {:d}".format(self._number_points))

    def getDataFromTime(self, time_seconds: float) -> None:
        logger.info("Getting data from {} seconds".format(time_seconds))

        i: int = 0

        for t in self.time:
            if t >= time_seconds:
                break
            i += 1

        logger.info("Index found: {}".format(i))
        logger.info("Value of time at index: {}".format(self.time[i]))
        logger.info(
            "Value of number of collisions at index: {}".format(self.total_col[i])
        )
        logger.info(
            "Value of collision average force at index: {}".format(
                self.avg_col_force_mag[i]
            )
        )

        logger.info("Updating arrays")
        self.time = self.time[i:]
        self.total_col = self.total_col[i:]
        self.avg_col_force_mag = self.avg_col_force_mag[i:]

        self._number_points = len(self.time)
        logger.info("Number of points: {}".format(self._number_points))

        # check if last values contains 0
        eps: float = 1.0e-12
        last_col: int = self.total_col[-1]
        last_force: float = self.avg_col_force_mag[-1]
        logger.info("Last time recorded: {}".format(self.time[-1]))
        logger.info("Last number of collision: {}".format(last_col))
        logger.info("Last collision force: {}".format(last_force))

        if (np.abs(last_col) < eps) or (np.abs(last_force) < eps):
            logger.info("Removing last row")
            self.time = self.time[:-1]
            self.total_col = self.total_col[:-1]
            self.avg_col_force_mag = self.avg_col_force_mag[:-1]

            self._number_points = len(self.time)
            logger.info("New number of points: {}".format(self._number_points))

            last_col = self.total_col[-1]
            last_force = self.avg_col_force_mag[-1]

            logger.info("New last time recorded: {}".format(self.time[-1]))
            logger.info("New last number of collision: {}".format(last_col))
            logger.info("New last collision force: {}".format(last_force))
