import json
import logging
import os
import pathlib
import re
import shutil
import sys
import threading
import time
import tkinter
from tkinter import font
from typing import Any, List, TypedDict

import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from . import csv_edem, csv_edem_controller, csv_edem_updater

logging.getLogger("matplotlib.font_manager").disabled = True

root = tkinter.Tk()
fonts = list(font.families())
fonts.extend(["Helvetica"])
fonts.sort()
root.destroy()


class SettingsDict(TypedDict):
    theme: str
    font: str
    font_size: int


__icon__ = sg.DEFAULT_WINDOW_ICON

script_folder: str = os.path.abspath(pathlib.Path(__file__).parent.absolute())
config_file: str = os.path.join(script_folder, "config_csv_edem.cfg")

DEFAULT_SETTINGS: SettingsDict = {
    "theme": "DarkBrown5",
    "font": "Helvetica",
    "font_size": 16,
}

##################### Load/Save Settings File #####################
def save_settings(settings_file: str, settings: SettingsDict) -> None:
    with open(settings_file, "w") as f:
        json.dump(settings, f)


def load_settings(settings_file: str, default_settings: SettingsDict) -> SettingsDict:
    settings: SettingsDict
    try:
        with open(settings_file, "r") as f:
            settings = json.load(f)
    except Exception as e:
        print("Creating default config file...")
        settings = default_settings
        save_settings(settings_file, settings)
    return settings


CURRENT_SETTINGS: SettingsDict = load_settings(config_file, DEFAULT_SETTINGS)

cf_theme: str = CURRENT_SETTINGS["theme"]
cf_font: str = CURRENT_SETTINGS["font"]
cf_font_size: int = int(CURRENT_SETTINGS["font_size"])

sg.theme(cf_theme)
sg.set_options(font=(cf_font, cf_font_size))
sg.SetGlobalIcon(__icon__)

fig_canvas_agg: FigureCanvasTkAgg = None


def csv_edem_main_thread(window: sg.Window, cmd_args: List[str]) -> None:
    c: csv_edem_controller.CSV_Edem_Controller = csv_edem.main(_args=cmd_args)
    try:
        time = c._input.time
        col = c._input.total_col
        forces = c._input.avg_col_force_mag
        window.write_event_value("-THREAD EXEC DONE-", [time, col, forces])
    except:
        window.write_event_value("-THREAD EXEC DONE-", "")


def draw_figure(canvas: tkinter.Canvas, figure: plt.Figure) -> FigureCanvasTkAgg:
    plt.close("all")  # erases previously drawn plots
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


def collapse(layout: List[List[Any]], key: str) -> sg.pin:
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key))


def sgModeRad(txt: str, key: str, default: bool = False) -> sg.Radio:
    return sg.Radio(text=txt, group_id=1, default=default, key=key, enable_events=True)


def sgSeparatorRad(txt: str, key: str, default: bool = False) -> sg.Radio:
    return sg.Radio(text=txt, group_id=2, default=default, key=key)


def spinIgnoreRows(key: str) -> sg.Spin:
    return sg.Spin(
        values=[i for i in range(0, 51)],
        initial_value=25,
        enable_events=True,
        size=(5, 1),
        k=key,
    )


def main() -> None:
    def csv_edem_call() -> None:
        threading.Thread(
            target=csv_edem_main_thread, args=(window, cmd_args), daemon=True
        ).start()

    def csv_edem_update_thread(window: sg.Window) -> None:
        csv_edem_updater.update()
        window.write_event_value("-THREAD UPDATE DONE-", "")

    def csv_edem_update_call() -> None:
        threading.Thread(
            target=csv_edem_update_thread, args=(window), daemon=True
        ).start()

    def plot_graphs(
        x_data: List[float],
        y_data: List[float],
        title: str,
        xlabel: str,
        ylabel: str,
        line: bool,
    ) -> None:

        fig: plt.Figure
        ax: plt.Axes
        fig, ax = plt.subplots()
        if line:
            ax.plot(x_data, y_data)
        else:
            ax.scatter(x_data, y_data)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        global fig_canvas_agg
        if fig_canvas_agg:
            fig_canvas_agg.get_tk_widget().forget()
        fig_canvas_agg = draw_figure(canvas_plot.TKCanvas, fig)

    section_single = [
        [
            sg.T("Arquivo CSV: "),
            sg.I(k="csv#input", enable_events=True),
            sg.FileBrowse(
                "...", file_types=(("Arquivos CSV", "*.csv"),), k="filebrowse_single"
            ),
            sg.B("Abrir arquivo", k="opencsv#button"),
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Col(
                [
                    [
                        sg.T("Arquivo Excel de saída: "),
                    ],
                    [sg.T("Arquivo TXT de saída: ")],
                ]
            ),
            sg.Col(
                [
                    [sg.I(k="out_excel#input"), sg.B("Abrir", k="out_excel#button")],
                    [sg.I(k="out_txt#input"), sg.B("Abrir", k="out_txt#button")],
                ]
            ),
        ],
    ]

    section_multi = [
        [sg.T("Diretório contendo múltiplos CSVs: ")],
        [
            sg.I(k="multicsv#input", enable_events=True),
            sg.FolderBrowse("...", k="folderbrowse_multi"),
            sg.B("Abrir diretório", k="open_multi_dir#button"),
        ],
        [sg.HorizontalSeparator()],
        [
            sg.B(
                "Abrir planilha resultante",
                k="multi_excel#button",
                tooltip="Clique em executar para habilitar este botão",
            )
        ],
    ]

    tab_options_layout = [
        [sg.HorizontalSeparator()],
        [
            sg.T("Modo: "),
            sgModeRad("Arquivo único", "single#rad", default=True),
            sgModeRad("Múltiplos arquivos", "multi#rad"),
        ],
        [sg.HorizontalSeparator()],
        [collapse(section_single, key="single#section")],
        [collapse(section_multi, key="multi#section")],
        [sg.HorizontalSeparator()],
        [
            sg.T("Diretório de saída: "),
            sg.I(k="output_dir#input"),
            sg.FolderBrowse("..."),
            sg.B("Abrir diretório", k="abrir_outdir#button"),
        ],
        [sg.HorizontalSeparator()],
    ]

    tab_app_config_layouyt = [
        [sg.HorizontalSeparator()],
        [sg.T("Configurações do aplicativo:")],
        [
            sg.T("Tema: "),
            sg.Combo(
                sg.theme_list(), default_value=cf_theme, k="theme#combo", readonly=True
            ),
        ],
        [
            sg.T("Fonte: "),
            sg.Combo(fonts, default_value=cf_font, k="font#combo", readonly=True),
        ],
        [
            sg.T("Tamanho da fonte: "),
            sg.Spin(
                values=[i for i in range(10, 51)],
                initial_value=int(cf_font_size),
                enable_events=True,
                size=(5, 1),
                k="font_size",
                readonly=True,
            ),
        ],
        [sg.HorizontalSeparator()],
        [sg.B("Salvar configurações", k="save_config#button")],
        [sg.HorizontalSeparator()],
    ]

    tab_advanced_options_layout = [
        [sg.HorizontalSeparator()],
        [
            sg.Checkbox(
                "Exportar médias logarítmicas", default=False, k="export_log#checkbox"
            )
        ],
        [sg.HorizontalSeparator()],
        [
            sg.T("Separador decimal: "),
            sgSeparatorRad("Vírgula", "virgula#rad", default=True),
            sgSeparatorRad("Ponto", "ponto#rad"),
        ],
        [sg.HorizontalSeparator()],
        [sg.T("Tempo de corte [segundos]: ")],
        [
            sg.Slider(
                range=(0.0, 50.0),
                default_value=1.01,
                resolution=0.01,
                orientation="h",
                k="cutoff#slider",
            )
        ],
        [sg.HorizontalSeparator()],
        [sg.T("Linhas para ignorar dos arquivos CSV: "), spinIgnoreRows("linhas#spin")],
        [sg.HorizontalSeparator()],
        [sg.B("Atualizar código do programa", k="atualizar#button")],
        [sg.HorizontalSeparator()],
    ]

    group_id_rad_plot_type = 3

    tab_plots_layout = [
        [sg.HorizontalSeparator()],
        [
            sg.T("Estilo dos gráficos"),
            sg.R("Linha", group_id=group_id_rad_plot_type, default=True, k="linha#rad"),
            sg.R("Pontos", group_id_rad_plot_type, k="pontos#rad"),
        ],
        [sg.HorizontalSeparator()],
        [sg.Canvas(k="plot#canvas")],
        [sg.HorizontalSeparator()],
        [
            sg.B("Tempo x Número de colisões", k="plot_col#button"),
            sg.T("    "),
            sg.B("Tempo x Força colisional", k="plot_for#button"),
        ],
        [sg.HorizontalSeparator()],
    ]

    tab_output_layout = [[sg.Output(echo_stdout_stderr=True, k="output#output")]]

    layout = [
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab("Principal", tab_options_layout, key="options#tab"),
                        sg.Tab(
                            "Opções avançadas",
                            tab_advanced_options_layout,
                            key="ad_options#tab",
                        ),
                        sg.Tab(
                            "Configurações", tab_app_config_layouyt, key="config#tab"
                        ),
                        sg.Tab("Output", tab_output_layout, key="output#tab"),
                        sg.Tab("Gráficos", tab_plots_layout, key="plots#tab"),
                    ]
                ],
                k="trabgroup",
            )
        ],
        [sg.B("Executar programa", k="exec#button", tooltip="Atalho: ctrl-r")],
        [sg.HorizontalSeparator()],
        [sg.StatusBar("", k="status#text", size=(30, 1), justification="r")],
    ]

    window = sg.Window(
        "CSV EDEM - Interface Gráfica",
        layout,
        resizable=True,
        return_keyboard_events=True,
        icon=__icon__,
        titlebar_icon=__icon__,
    )
    window.finalize()
    window.set_min_size((1000, 500))

    output_txt: sg.Output = window["output#output"]
    excel_multi_button: sg.Button = window["multi_excel#button"]
    exec_button: sg.Button = window["exec#button"]
    update_button: sg.Button = window["atualizar#button"]
    canvas_plot: sg.Canvas = window["plot#canvas"]

    output_txt.expand(expand_x=True, expand_y=True)
    canvas_plot.expand(expand_x=True, expand_y=True)
    window["trabgroup"].expand(expand_x=True, expand_y=True)

    status_clean_time: float = 3.0
    status_t0: float = time.time()
    can_clean_status: bool = False
    old_multi_dir: str = ""

    #  visibility
    window["single#section"].update(visible=True)
    window["multi#section"].update(visible=False)
    excel_multi_button.update(disabled=True)

    # redirect log output to window
    root_logger: logging.Logger = logging.getLogger()
    handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)

    single_data_ready: bool = False
    multi_data_read: bool = False
    sindle_csv_old: str = ""
    multi_csv_old: str = ""

    while True:

        event, values = window.read(timeout=333)

        if event == sg.WIN_CLOSED or event == "Exit":
            break

        if event == "abrir_outdir#button":
            out_dir = values["output_dir#input"]
            if os.path.isdir(out_dir):
                os.startfile(out_dir)

        if event == "opencsv#button":
            csv = values["csv#input"]
            if os.path.isfile(csv):
                os.startfile(csv)

        if event == "linhas#spin":
            window[event].update(re.sub(r"[^0-9]", "", str(values[event])))
            window.refresh()

        if event == "atualizar#button":
            window["status#text"].update("Atualizando...")
            can_clean_status = False
            update_button.update(disabled=True)
            exec_button.update(disabled=True)

            csv_edem_update_call()

        if event == "-THREAD UPDATE DONE-":
            update_button.update(disabled=False)
            exec_button.update(disabled=False)
            window["status#text"].update("Atualizado!")
            can_clean_status = True
            status_t0 = time.time()

        if event in ("single#rad", "multi#rad"):
            if values["single#rad"]:
                window["single#section"].update(visible=True)
                window["multi#section"].update(visible=False)
            else:
                window["single#section"].update(visible=False)
                window["multi#section"].update(visible=True)

        if event == "multi_excel#button":
            f = os.path.join(values["output_dir#input"], "batch_EDEM_files.xlsx")
            if os.path.isfile(f):
                os.startfile(f)

        if event == "exec#button":

            go_on = True

            # check outputdir
            output_dir = values["output_dir#input"]
            if not os.path.isdir(output_dir):
                sg.PopupOK(
                    f"Diretório não existe:\n{output_dir}", title="Diretório inválido"
                )
                go_on = False

            else:
                # check inputs
                if values["single#rad"]:
                    csv_file = values["csv#input"]
                    if (not os.path.isfile(csv_file)) or (
                        os.path.splitext(csv_file)[-1].lower() != ".csv"
                    ):
                        sg.PopupOK(
                            f"Arquivo CSV inválido:\n{csv_file}", title="CSV inválido"
                        )
                        go_on = False
                else:
                    multi_dir = values["multicsv#input"]
                    if not os.path.isdir(multi_dir):
                        sg.PopupOK(
                            f"Diretório não existe:\n{multi_dir}",
                            title="Diretório inválido",
                        )
                        go_on = False

            if go_on:
                single_data_ready = False
                can_clean_status = False
                window["status#text"].update("Computando...")
                exec_button.update(disabled=True)
                update_button.update(disabled=True)

                # Limpar output
                output_txt.update("", visible=True)
                window.refresh()

                # preparar comando
                cmd_args = []

                # comandos gerais
                # -t
                cmd_args.append("-t")
                cmd_args.append(f'{values["cutoff#slider"]:.5f}')
                # -n
                if values["ponto#rad"]:
                    cmd_args.append("--no-comma")
                # -l
                if values["export_log#checkbox"]:
                    cmd_args.append("--log")
                # -r
                cmd_args.append("--skip_rows")
                cmd_args.append(f'{int(values["linhas#spin"])}')

                # Single
                if values["single#rad"]:
                    cmd_args.append("-s")
                    cmd_args.append(csv_file)
                    cmd_args.append("-e")
                    cmd_args.append(os.path.join(output_dir, values["out_excel#input"]))
                    cmd_args.append("--summary")
                    cmd_args.append(os.path.join(output_dir, values["out_txt#input"]))
                else:
                    # gen input
                    excel_multi_button.update(disabled=True)
                    window.refresh()
                    os.chdir(multi_dir)
                    input_txt = os.path.join(output_dir, "input.txt")
                    csv_edem.main(_args=["--gen_batch", input_txt])

                    cmd_args.append("--batch")
                    cmd_args.append(input_txt)

                # call script
                csv_edem_call()

            else:
                window.write_event_value("-THREAD EXEC ERROR-", "")

        if event == "multicsv#input":
            multi_dir = os.path.abspath(values[event])
            window[event].update(multi_dir)
            output_dir = multi_dir
            window["output_dir#input"].update(output_dir)
            if multi_dir != old_multi_dir:
                excel_multi_button.update(disabled=True)
                old_multi_dir = multi_dir
            window.refresh()

        if event == "-THREAD EXEC DONE-":
            if values["multi#rad"]:
                output_dir = values["output_dir#input"]
                multi_dir = values["multicsv#input"]
                # copy excel to output dir if output_dir != multi_folder
                if multi_dir != output_dir:
                    shutil.copy(
                        os.path.join(multi_dir, "batch_EDEM_files.xlsx"), output_dir
                    )

            else:  # single mdoe
                ret = values[event]

            window["status#text"].update("Terminado!")
            exec_button.update(disabled=False)
            update_button.update(disabled=False)
            single_data_ready = True
            can_clean_status = True
            status_t0 = time.time()

        if event == "-THREAD EXEC ERROR-":
            window["status#text"].update("Erro!")
            status_t0 = time.time()
            can_clean_status = True

        if event == "csv#input":
            single_data_ready = False
            csv = os.path.abspath(values[event])
            window[event].update(csv)
            dir_csv = os.path.dirname(csv)
            basename_csv = os.path.splitext(os.path.basename(csv))[0]

            window["out_excel#input"].update(basename_csv)
            window["out_txt#input"].update(basename_csv)
            window["output_dir#input"].update(dir_csv)

            window.refresh()

        if event == "open_multi_dir#button":
            multi_dir = values["multicsv#input"]
            if os.path.isdir(multi_dir):
                os.startfile(multi_dir)

        if event == "out_excel#button":
            f = os.path.join(
                values["output_dir#input"], values["out_excel#input"] + ".xlsx"
            )
            if os.path.isfile(f):
                os.startfile(f)

        if event == "out_txt#button":
            f = os.path.join(
                values["output_dir#input"], values["out_txt#input"] + ".txt"
            )
            if os.path.isfile(f):
                os.startfile(f)

        if event == "save_config#button":
            try:
                CURRENT_SETTINGS["theme"] = str(values["theme#combo"])
                CURRENT_SETTINGS["font"] = str(values["font#combo"])
                CURRENT_SETTINGS["font_size"] = int(values["font_size"])

                save_settings(config_file, CURRENT_SETTINGS)
                window["status#text"].update("Salva! É necessário reiniciar o app!")
            except:
                window["status#text"].update("Erro ao salvar configurações!")
            status_t0 = time.time()
            can_clean_status = True

        # atalhos de teclas
        if event == "r:82":  # ctrl-r
            window["exec#button"].click()

        if event == "o:79":  # ctrl-o
            if values["single#rad"]:
                window["filebrowse_single"].click()
            else:
                window["folderbrowse_multi"].click()

        if event == "1:49":
            window["options#tab"].select()

        if event == "2:50":
            window["ad_options#tab"].select()

        if event == "3:51":
            window["config#tab"].select()

        if event == "4:52":
            window["output#tab"].select()

        if event == "plot_col#button":
            if values["single#rad"]:
                plt.close()
                title: str = f"Número de colisões\nmáx.: {np.max(ret[1])}    mín.: {np.min(ret[1])}"
                xlabel: str = "Tempo [segundos]"
                ylabel: str = "[-]"
                plot_graphs(ret[0], ret[1], title, xlabel, ylabel, values["linha#rad"])

        if event == "plot_for#button":
            if values["single#rad"]:
                title = f"Força colisional\nmáx.: {np.max(ret[2]):.3f}    mín.: {np.min(ret[2]):.3f}"
                xlabel = "Tempo [segundos]"
                ylabel = "Força [N]"
                plot_graphs(ret[0], ret[2], title, xlabel, ylabel, values["linha#rad"])

        # atualizar botões
        if values["single#rad"]:
            out_dir = values["output_dir#input"]
            excel = os.path.join(out_dir, values["out_excel#input"] + ".xlsx")
            txt = os.path.join(out_dir, values["out_txt#input"] + ".txt")
            window["out_excel#button"].update(disabled=not os.path.isfile(excel))
            window["out_txt#button"].update(disabled=not os.path.isfile(txt))

        # atualizar botões
        if values["multi#rad"]:
            multi_excel = os.path.join(
                values["output_dir#input"], "batch_EDEM_files.xlsx"
            )
            excel_multi_button.update(disabled=not os.path.isfile(multi_excel))

        window["plot_for#button"].update(
            disabled=(not single_data_ready) or (not values["single#rad"])
        )
        window["plot_col#button"].update(
            disabled=(not single_data_ready) or (not values["single#rad"])
        )

        # limpa status bar
        if can_clean_status and ((time.time() - status_t0) >= status_clean_time):
            window["status#text"].update("")

    window.close()


if __name__ == "__main__":
    main()
