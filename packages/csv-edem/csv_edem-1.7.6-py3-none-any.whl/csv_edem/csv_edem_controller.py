import logging
from datetime import date

import numpy as np

from . import csv_input, utils

logger = logging.getLogger(__name__)


class CSV_Edem_Controller:
    def __init__(self, inputCSV: csv_input.CSV_Edem_input):
        logger.info(
            "Creating object CSV_Edem_Controller with csv file '{}'".format(
                inputCSV.getFilename()
            )
        )
        self._input = inputCSV

        self._min_time: float = 0.0
        self._max_time: float = 0.0

        self._min_col: float = 0.0
        self._max_col: float = 0.0

        self._min_for: float = 0.0
        self._max_for: float = 0.0

        self._mean_col: float = 0.0
        self._logmean_col: float = 0.0

        self._mean_for: float = 0.0
        self._logmean_for: float = 0.0

        self._export_log = False

        self.computeParameters()

    def saveToExcel(self, excel_filename: str) -> None:
        logger.info("saveToExcel called with argument '{}'".format(excel_filename))

        filename = excel_filename + ".xlsx"
        sheetname = "edem_data"

        headers = [
            "Time [seconds]",
            "Total Number of Collisions [-]",
            "Average Collision Normal Force Magnitude [N]",
        ]
        data = np.transpose(
            np.array(
                [self._input.time, self._input.total_col, self._input.avg_col_force_mag]
            )
        )

        utils.saveDataToExcel(filename, data, headers, sheetname=sheetname)

        return

    def getMeanCol(self) -> float:
        return self._mean_col

    def getLogMeanCol(self) -> float:
        return self._logmean_col

    def getMeanForce(self) -> float:
        return self._mean_for

    def getLogMeanForce(self) -> float:
        return self._logmean_for

    def computeParameters(self) -> None:
        logger.info("computeParameters method called")
        self._min_time = np.min(self._input.time)
        self._max_time = np.max(self._input.time)

        self._min_col = np.min(self._input.total_col)
        self._max_col = np.max(self._input.total_col)

        self._mean_col = float(np.mean(self._input.total_col))
        self._logmean_col = (self._max_col - self._min_col) / np.log(
            self._max_col / self._min_col
        )

        self._min_for = np.min(self._input.avg_col_force_mag)
        self._max_for = np.max(self._input.avg_col_force_mag)

        self._mean_for = float(np.mean(self._input.avg_col_force_mag))
        self._logmean_for = (self._max_for - self._min_for) / np.log(
            self._max_for / self._min_for
        )

    def saveSummary(
        self,
        summary_filename: str,
        useCommaAsDecimal: bool = False,
        export_log: bool = False,
    ) -> None:
        logger.info("saveSummary called with argument '{}'".format(summary_filename))
        logger.info("useCommaAsDecimal: {}".format(useCommaAsDecimal))

        if export_log:
            logger.info("Exporting log mean information")
        else:
            logger.info("Not exporting log mean information")

        decimal_sep: str = "," if useCommaAsDecimal else "."

        content: str = ""
        content += "Input file: {}\n".format(self._input.getFilename())
        content += "Date: {} \n\n".format(date.today().strftime("%d-%b-%Y"))

        content += "Minimum time: {} seconds\n".format(self._min_time).replace(
            ".", decimal_sep
        )
        content += "Maximum time: {} seconds\n\n".format(self._max_time).replace(
            ".", decimal_sep
        )

        content += "Minimum collision: {}\n".format(self._min_col).replace(
            ".", decimal_sep
        )
        content += "Maximum collision: {}\n".format(self._max_col).replace(
            ".", decimal_sep
        )
        content += "Mean collision: {:.2f}\n".format(self._mean_col).replace(
            ".", decimal_sep
        )

        if export_log:
            content += "Log mean collision: {:.2f}\n".format(self._logmean_col).replace(
                ".", decimal_sep
            )

        content += "\n"

        content += "Minimum collision force: {:.8f} N\n".format(self._min_for).replace(
            ".", decimal_sep
        )
        content += "Maximum collision force: {:.8f} N\n".format(self._max_for).replace(
            ".", decimal_sep
        )
        content += "Mean collision force: {:.8f} N\n".format(self._mean_for).replace(
            ".", decimal_sep
        )

        if export_log:
            content += "Log mean collision force: {:.8f} N\n".format(
                self._logmean_for
            ).replace(".", decimal_sep)

        content += "\n"

        output_file: str = summary_filename + ".txt"
        with open(output_file, "w") as f:
            f.write(content)

        logger.info("Content of '{}':\n\n{}".format(output_file, content))
