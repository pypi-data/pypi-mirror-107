import argparse
import logging
import os
import time
from collections.abc import Callable
from pathlib import Path
from typing import List, Optional

import numpy as np

from . import csv_edem_controller, csv_input, utils

logger = logging.getLogger(__name__)


class CSV_Edem_Batch:
    def __init__(self, input_file: str, args: argparse.Namespace):
        logger.info(
            "Creating object CSV_Edem_Batch with input file '{}'".format(input_file)
        )

        self._input_file = input_file
        self._files: List[str] = []
        self._number_files: int = 0

        self.args: argparse.Namespace = args

        self.mean_cols: np.ndarray = np.array([])
        self.logmean_cols: np.ndarray = np.array([])

        self.mean_fors: np.ndarray = np.array([])
        self.logmean_fors: np.ndarray = np.array([])

        self._export_log: bool = self.args.log

        # check if batch file exists
        if not os.path.isfile(self._input_file):
            logger.warn(
                'Batch mode input file "{}" does not exist'.format(self._input_file)
            )
            return

        self.extractFiles()

    def extractFiles(self) -> None:
        logger.info("extractFiles method called")
        with open(self._input_file) as f:
            content = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        self._files = [x.strip() for x in content if utils.isValidCSV(x.strip())]
        logger.info("Files found:\n\t\t\t{}".format(self._files))
        self._number_files = len(self._files)
        logger.info("Number of files: {}".format(self._number_files))

    def executeBatch(
        self, callback: Optional[Callable[[str, int, bool], None]] = None
    ) -> None:
        logger.info("executeBatch method called")

        skip: int = int(self.args.skip_rows[0])
        cut_time: float = float(self.args.cut_time[0])

        # allocate room for np arrays
        self.mean_cols = np.zeros(self._number_files, dtype=np.float32)
        self.logmean_cols = np.zeros(self._number_files, dtype=np.float32)

        self.mean_fors = np.zeros(self._number_files, dtype=np.float32)
        self.logmean_fors = np.zeros(self._number_files, dtype=np.float32)

        logger.info("Looping through each file")

        for i, file in enumerate(self._files):
            # call input
            if callback is not None:
                callback(file, i + 1, False)

            inpt = csv_input.CSV_Edem_input(file, lines_to_skip=skip)
            basename_input = os.path.splitext(inpt.getFilename())[0]
            excel_file: str = (
                basename_input if (self.args.excel == "excel") else self.args.excel
            )
            summary_file: str = (
                basename_input
                if (self.args.summary == "summary")
                else self.args.summary
            )

            # Check if file exists
            if not inpt.checkIfFileExists():
                logger.warning("File '{}' does not exists!!".format(inpt.getFilename()))
                return

            inpt.extractRawData()
            inpt.getDataFromTime(cut_time)

            cntrllr = csv_edem_controller.CSV_Edem_Controller(inpt)

            self.mean_cols[i] = cntrllr.getMeanCol()
            self.logmean_cols[i] = cntrllr.getLogMeanCol()
            self.mean_fors[i] = cntrllr.getMeanForce()
            self.logmean_fors[i] = cntrllr.getLogMeanForce()

            if callback is not None:
                callback(file, i + 1, True)
                time.sleep(0.1)

    def getHeaders(self) -> List[str]:
        if self._export_log:
            return [
                "File",
                "Collision Number - Mean [-]",
                "Collision Number - Log Mean [-]",
                "Collision Normal Force Magnitude - Mean [N]",
                "Collision Normal Force Magnitude - Log Mean [N]",
            ]
        else:
            return [
                "File",
                "Collision Number - Mean [-]",
                "Collision Normal Force Magnitude - Mean [N]",
            ]

    def getFiles(self) -> List[str]:
        return self._files

    def getNumberOfFiles(self) -> int:
        return len(self._files)

    def getMeanCollisons(self) -> np.ndarray:
        return self.mean_cols

    def getMeanOfNormalCollisions(self) -> float:
        return float(np.mean(self.mean_cols))

    def getMeanOfNormalForces(self) -> float:
        return float(np.mean(self.mean_fors))

    def getMeanOfLogCollisions(self) -> float:
        return float(np.mean(self.logmean_cols))

    def getMeanOfLogForces(self) -> float:
        return float(np.mean(self.logmean_fors))

    def isExportingLog(self) -> bool:
        return self._export_log

    def getData(self) -> np.ndarray:
        if self._export_log:
            data = np.transpose(
                np.array(
                    [
                        [Path(f).name for f in self._files],
                        self.mean_cols,
                        self.logmean_cols,
                        self.mean_fors,
                        self.logmean_fors,
                    ]
                )
            )
        else:
            data = np.transpose(
                np.array(
                    [
                        [Path(f).name for f in self._files],
                        self.mean_cols,
                        self.mean_fors,
                    ]
                )
            )
        return data

    def saveToExcel(self, excel_filename: str) -> None:
        logger.info("saveToExcel called with argument '{}'".format(excel_filename))

        filename = excel_filename + ".xlsx"
        sheetname = "edem_batch_data"

        headers = self.getHeaders()
        data = self.getData()

        if self._export_log:
            logger.info("Exporting log mean information")
        else:
            logger.info("Not exporting log mean information")

        column_widths: List[int] = []
        align: List[str] = []

        column_widths.append(len(data[0, 0]) + 10)
        align.append("left")

        for i, header in enumerate(headers):
            if i > 0:
                column_widths.append(len(header))
                align.append("right")

        utils.saveDataToExcel(
            filename,
            data,
            headers,
            sheetname=sheetname,
            column_widths=column_widths,
            align=align,
        )

        return
