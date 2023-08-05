# v1.0.0

import logging
import os
import pathlib
import shutil
import time
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile

logger = logging.getLogger("csv_update")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s: %(message)s")


def getVersion(filename: str) -> str:

    first_line = ""
    with open(filename, "r") as f:
        first_line = f.readline()

    first_line = first_line.strip("\n").strip("#").strip()
    return first_line


def update() -> None:

    start_time = time.time()
    # =======================================================

    logger.info("Update started")

    current_file_path = pathlib.Path(__file__).parent.absolute()
    os.chdir(current_file_path)

    logger.info(f'Changed path to "{current_file_path}"')

    zipurl = "https://github.com/marcusbfs/csv_edem/archive/main.zip"

    logger.info("ZIP URL: {}".format(zipurl))

    tmp_folder = os.path.join(os.path.abspath("."), "tmp")
    src_folder = os.path.join(tmp_folder, "csv_edem-main")
    dst_folder = os.path.abspath("..")

    logger.info('tmp_folder: "{}"'.format(tmp_folder))
    logger.info('src_folder: "{}"'.format(src_folder))
    logger.info('dst_folder: "{}"'.format(dst_folder))

    logger.info("Downloading zip...")

    with urlopen(zipurl) as zipresp:
        with ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall("./tmp")

    logger.info('Zip downloaded and extracted to "{}"'.format(tmp_folder))

    # check updater version

    first_line = ""
    with open(os.path.join(src_folder, "csv_edem", "csv_edem_updater.py"), "r") as f:
        first_line = f.readline()

    first_line = first_line.strip("\n")

    updater_file_name = "csv_edem_updater.py"

    current_updater = os.path.join(os.path.abspath("."), updater_file_name)
    new_updater = os.path.join(src_folder, "csv_edem", updater_file_name)

    current_version = getVersion(current_updater)
    new_version = getVersion(new_updater)

    if current_version != new_version:
        logger.info('Current version: "{}"'.format(current_version))
        logger.info('New version: "{}"'.format(new_version))
        logger.info("Theres a new updater!")
        shutil.move(new_updater, current_updater)
        logger.info("Executing new updater...\n")
        exec(open(updater_file_name).read())
        return

    input_examples_dir = os.path.join(os.path.abspath(".."), "inputs_examples")
    if not os.path.isdir(input_examples_dir):
        logger.info('Creating directory "{}"'.format(input_examples_dir))
        os.mkdir(input_examples_dir)

    logger.info('Using "shutil.move" command')

    _file: str
    for _file in os.listdir(src_folder):
        src: str = os.path.join(src_folder, _file)
        dst: str = os.path.join(dst_folder, _file)
        if os.path.isdir(src):
            for subf in os.listdir(src):
                sub_src = os.path.join(src, subf)
                sub_dst = os.path.join(dst, subf)
                logger.info('Moving "{}" to "{}"'.format(sub_src, sub_dst))
                shutil.move(sub_src, sub_dst)
        elif os.path.isfile(src):
            logger.info('Moving "{}" to "{}"'.format(src, dst))
            shutil.move(src, dst)

    logger.info('Removing "{}"'.format(tmp_folder))
    shutil.rmtree(tmp_folder, ignore_errors=True)

    # =======================================================

    time.time()

    logger.info("Update finished in {:.3f} seconds".format(time.time() - start_time))


if __name__ == "__main__":
    update()
