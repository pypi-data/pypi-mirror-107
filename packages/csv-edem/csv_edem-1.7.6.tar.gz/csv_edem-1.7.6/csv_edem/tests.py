import logging

from . import csv_edem_controller, csv_input

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s: %(message)s")

filename = "inputs_examples/C1.csv"

input1 = csv_input.CSV_Edem_input(filename)

if not input1.checkIfFileExists():
    print("File '{}' does not exists".format(input1.getFilename()))
    exit()


input1.extractRawData()

input1.getDataFromTime(1.01)


controller = csv_edem_controller.CSV_Edem_Controller(input1)


controller.saveToExcel("dados_c1")
controller.saveSummary("dados_c1")
