from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, List

import numpy as np
from rich.progress import BarColumn, Progress, SpinnerColumn, TimeRemainingColumn, track
from rich.table import Table

from . import __version__, csv_edem_batch, csv_edem_controller, csv_input, utils
from .rich_console import console

logger = logging.getLogger("csv_edem")

INPUT_TXT_DEFAULT = "input_csv_edem.txt"


def gen_input_txt(gen_dir: Path, input_file: str, info: bool = False) -> None:

    console.print(f'Generating files from "{str(gen_dir)}"')

    csv_files_in_curr_dir = [f for f in gen_dir.iterdir() if utils.isValidCSV(str(f))]
    i = 1
    with open(input_file, "w") as outf:
        for csv in track(
            csv_files_in_curr_dir, description="Getting files...", transient=True
        ):
            time.sleep(0.1)
            outf.write(str(csv))
            outf.write(os.linesep)

    console.print(f"Found [bold blue]{len(csv_files_in_curr_dir)}[/] files:")
    if not info:
        for csv in csv_files_in_curr_dir:
            f = Path(os.curdir).resolve() / csv
            console.print(f'  {i:02d} - "{f}"')
            i += 1

    logger.info('"{}" generated'.format(input_file))


def batch_input_txt(
    input_file: str, args: argparse.Namespace, info: bool = False
) -> None:

    # check if batch file exists
    if not os.path.isfile(input_file):
        logger.warning('Batch mode input file "{}" does not exist'.format(input_file))
        return

    batch_ctrller = csv_edem_batch.CSV_Edem_Batch(input_file, args)

    if not info:
        progress = Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            "{task.fields[extra]}",
            console=console,
            transient=True,
        )
        task = progress.add_task(
            total=batch_ctrller.getNumberOfFiles(),
            description="Processing...",
            extra="",
        )
        progress.start()

        def callback_fun(file: str, file_id: int, finished: bool) -> None:
            if finished:
                progress.update(task, advance=1, extra="")
            else:
                progress.update(task, extra=f"[dim]{file_id:2d} - {Path(file).name}")

    batch_ctrller.executeBatch(callback=callback_fun if not info else None)
    time.sleep(0.1)
    if not info:
        progress.stop()
    excel_file: str = "batch_EDEM_files"
    batch_ctrller.saveToExcel(excel_file)

    # show rich table
    headers = batch_ctrller.getHeaders()
    n_of_headers = len(headers)
    data = batch_ctrller.getData()
    table = Table()

    footers_fmt = "[bold green]"
    mean_row = [f"{footers_fmt}Mean" for _ in range(n_of_headers)]
    max_row = [f"{footers_fmt}Max" for _ in range(n_of_headers)]
    min_row = [f"{footers_fmt}Min" for _ in range(n_of_headers)]

    console.print(f"[bold blue]{Path(data[0,0]).parent.resolve()}")

    for i, header in enumerate(headers):
        if i == 0:
            table.add_column(header, justify="left")
        else:
            table.add_column(header, justify="right")
            row_data = [float(d) for d in data[:, i]]
            max_row[i] = f"{footers_fmt}{np.max(row_data):.5f}"
            min_row[i] = f"{footers_fmt}{np.min(row_data):.5f}"
            mean_row[i] = f"{footers_fmt}{np.mean(row_data):.5f}"

    for i in range(len(data)):
        data[i, 0] = str(Path(data[i, 0]).name)
        for j in range(1, n_of_headers):
            data[i, j] = f"{float(data[i,j]):.5f}"
        table.add_row(*data[i], end_section=(i == len(data) - 1))

    table.add_row(*mean_row)
    table.add_row(*max_row)
    table.add_row(*min_row)
    console.print(table)


def main(_args: List[str] = None) -> Any:

    default_skip_rows: int = 25
    default_cut_time: float = 1.01

    start_time = time.time()

    version_message = (
        "CSV EDEM reporter "
        + __version__
        + os.linesep
        + "Author: {}".format("Marcus Bruno Fernandes Silva")
        + os.linesep
        + "email: {}".format("marcusbfs@gmail.com")
    )

    desc = (
        version_message
        + os.linesep
        + os.linesep
        + "Process EDEM CSV files."
        + os.linesep
        + "Created for Gabi <3"
    )

    parser = argparse.ArgumentParser(
        description=desc, formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-s",
        "--single-file",
        dest="csv_file",
        nargs=1,
        help="single CSV EDEM file name with three columns: 1º time; 2º number of collisions; and 3º average force magnitude",
    )

    parser.add_argument(
        "-e",
        default="excel",
        dest="excel",
        help="base of the name of the excel file to be exported",
    )

    parser.add_argument(
        "--summary",
        default="summary",
        dest="summary",
        help="base of the name of the summary file to be exported",
    )

    parser.add_argument(
        "-n",
        "--no-comma",
        action="store_true",
        dest="no_comma",
        help="do not use comma (',') to separate decimal places (use '.')",
    )

    parser.add_argument(
        "-g",
        "--gen_batch",
        dest="gen_batch",
        nargs="?",
        default=".",
        help=f"generate input ({INPUT_TXT_DEFAULT}) file for batch mode",
    )

    parser.add_argument(
        "-b",
        "--batch",
        dest="batch",
        nargs="?",
        default=INPUT_TXT_DEFAULT,
        help=f'treat batch files. BATCH is a input file containing the CSV files in order to be processed. Default value is "{INPUT_TXT_DEFAULT}"',
    )

    parser.add_argument(
        "-B",
        dest="B",
        nargs="?",
        default=".",
        help=f"same as -g followed by -b",
    )

    parser.add_argument(
        "-l",
        "--log",
        action="store_true",
        dest="log",
        default=False,
        help="Exports log means as well",
    )

    parser.add_argument(
        "-t",
        dest="cut_time",
        nargs=1,
        default=[1.01],
        help="cut off time. Default value is {:.3f}".format(default_cut_time),
    )

    parser.add_argument(
        "-r",
        "--skip_rows",
        dest="skip_rows",
        nargs=1,
        default=[default_skip_rows],
        help="number of rows to skip. Default value is {}".format(default_skip_rows),
    )

    parser.add_argument(
        "-u",
        "--update",
        dest="update",
        default=False,
        help="update source code",
        action="store_true",
    )

    parser.add_argument(
        "--info",
        dest="info",
        default=False,
        help="Print aditional information",
        action="store_true",
    )

    parser.add_argument("-v", "--version", action="version", version=version_message)

    if _args:
        sys.argv = _args

    args = parser.parse_args(args=_args)
    level = logging.WARNING if not args.info else logging.INFO
    info = level == logging.INFO

    logging.basicConfig(level=level, format="%(asctime)s - %(name)s: %(message)s")

    logger.info("Arguments passed: {}".format(args))

    status_message = "Processing..."
    status = console.status(status_message)

    if args.update:
        logger.info("Calling update script...\n")

        from . import csv_edem_updater

        csv_edem_updater.update()

        return 0

    if "-B" in sys.argv:
        logger.info(f"-B called with args {args.B}")
        bdir: Path = Path(".").resolve() if (args.B is None) else Path(args.B).resolve()

        gen_input_txt(bdir, INPUT_TXT_DEFAULT, info=info)
        console.rule()
        batch_input_txt(INPUT_TXT_DEFAULT, args, info=info)

        logger.info(f"Removing {INPUT_TXT_DEFAULT}")
        os.remove(INPUT_TXT_DEFAULT)

        return 0

    elif ("-g" in sys.argv) or ("--gen_batch" in sys.argv):
        logger.info(
            'Generate batch file mode called with arg "{}"'.format(args.gen_batch)
        )
        gen_dir: Path = (
            Path(".").resolve()
            if (args.gen_batch is None)
            else Path(args.gen_batch).resolve()
        )
        gen_input_txt(gen_dir, INPUT_TXT_DEFAULT, info=info)

    elif ("-b" in sys.argv) or ("--batch" in sys.argv):
        input_file = INPUT_TXT_DEFAULT if (args.batch is None) else args.batch
        logger.info('Batch mode called with arg "{}"'.format(input_file))
        batch_input_txt(input_file, args, info)

    elif ("-s" in sys.argv) or ("--single-file" in sys.argv):
        if not info:
            status.start()

        logger.info("Single file mode")

        # call input
        skip: int = int(args.skip_rows[0])
        cut_time: float = float(args.cut_time[0])

        inpt = csv_input.CSV_Edem_input(args.csv_file[0], lines_to_skip=skip)
        basename_input = os.path.splitext(inpt.getFilename())[0]

        excel_file = basename_input if (args.excel == "excel") else args.excel
        summary_file: str = (
            basename_input if (args.summary == "summary") else args.summary
        )

        # Check if file exists

        if not inpt.checkIfFileExists():
            logger.warning("File '{}' does not exists!!".format(inpt.getFilename()))
            return 1

        inpt.extractRawData()
        inpt.getDataFromTime(cut_time)

        cntrllr = csv_edem_controller.CSV_Edem_Controller(inpt)

        # save
        cntrllr.saveSummary(
            summary_file, useCommaAsDecimal=not args.no_comma, export_log=args.log
        )
        cntrllr.saveToExcel(excel_file)
        # return cntrllr

        try:
            txt_file = summary_file + ".txt"
            with open(txt_file, "r") as tf:
                content = tf.read()
                console.print(content)
        except:
            pass

        if not info:
            status.stop()

    logger.info("Program finished in {:.3f} seconds".format(time.time() - start_time))

    return 0


if __name__ == "__main__":
    main()
