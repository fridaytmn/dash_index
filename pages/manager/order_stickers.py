import templates.flash
from queries import FILE_PATH
from utils.excel_processing import find_cell_by_value, get_value_by_location
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc, no_update, _dash_renderer
import utils.table_format
import pandas as pd
from app import app
import dash_mantine_components as dmc

_dash_renderer._set_react_version("18.2.0")

label = "Заказ наклеек"

note = """
Тут можно заказать наклейки на склад.
"""


def get_content() -> list:
    sticker_list = pd.read_excel(FILE_PATH).iloc[:, 5].dropna().astype(str).unique()

    return [
        dmc.MantineProvider(
            children=[
                html.Div(
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("Наименование"),
                                    dmc.Select(
                                        id="manager_order_sticker",
                                        data=sticker_list,
                                        placeholder="Выберите наклейку",
                                        searchable=True,
                                        clearable=True,
                                        w="450px",
                                    ),
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.Label("Расход за весь период, шт."),
                                    dbc.Input(
                                        id="manager_order_sticker_expense_count",
                                        disabled=True,
                                        type="text",
                                    ),
                                ]
                            ),
                            dbc.Col(
                                [
                                    html.Label("Кол-во по заказу*"),
                                    dbc.Input(
                                        id="manager_order_sticker_count",
                                        type="number",
                                        min=0,
                                        style={"min-width": "120px", "display": "flex"},
                                    ),
                                ]
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Добавить в список",
                                    id="manager_update_sticker_add",
                                    style={
                                        "margin-top": "5px",
                                        "background-color": "#acd180",
                                        "min-width": "170px",
                                    },
                                ),
                                width="auto",
                            ),
                        ],
                        align="end",
                    ),
                    className="form-inline-wrapper",
                ),
                html.Div(id="save_new_storage_sticker"),
                dcc.Store(id="manager_order_sticker_table_store", data=[]),
                html.Div(id="manager_order_sticker_table_wrapper"),
            ]
        )
    ]


@app.callback(
    Output("manager_order_sticker_expense_count", "value"),
    Input("manager_order_sticker", "value"),
    prevent_initial_call=True,
)
def fill_expense(sticker):
    if not sticker:
        return ""

    location = find_cell_by_value(
        filename=FILE_PATH, search_value=sticker, number_column=5
    )

    if not location:
        return ""

    return get_value_by_location(FILE_PATH, row=location[0], column=location[1] + 8)


@app.callback(
    Output("manager_order_sticker_table_store", "data", allow_duplicate=True),
    Output("manager_order_sticker_table_wrapper", "children", allow_duplicate=True),
    Output("save_new_storage_sticker", "children", allow_duplicate=True),
    Input("manager_update_sticker_add", "n_clicks"),
    State("manager_order_sticker", "value"),
    State("manager_order_sticker_expense_count", "value"),
    State("manager_order_sticker_count", "value"),
    State("manager_order_sticker_table_store", "data"),
    prevent_initial_call=True,
)
def add_sticker(_, sticker, expense, count, stored):  # noqa C901
    stored = list(stored or [])

    if not sticker or count is None:
        return (
            stored,
            no_update,
            templates.flash.render("", "Заполните наименование и количество"),
        )

    try:
        count = int(count)
        expense = int(expense or 0)
    except ValueError:
        return (
            stored,
            no_update,
            templates.flash.render("", "Количество должно быть целым числом"),
        )

    if any(row["Наименование"] == sticker for row in stored):
        return (
            stored,
            no_update,
            templates.flash.render("", "Эта наклейка уже добавлена"),
        )

    row = {
        "Наименование": sticker,
        "Расход за весь период, шт": expense,
        "Кол-во по заказу, шт": count,
        "Доп на склад, шт": 0,
        "Всего к заказу, шт": count,
    }

    stored.append(row)
    df = pd.DataFrame(stored)

    return (
        stored,
        get_table(df),
        templates.flash.render("", f"Наклейка «{sticker}» добавлена", color="#acd180"),
    )


@table_wrapper()
def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        columns=columns,
        data=data.to_dict("records"),
        style_cell_conditional=styles,
        sort_action="custom",
        sort_by=[],
        page_size=50,
        row_deletable=True,
    )
