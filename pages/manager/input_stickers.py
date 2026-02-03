import templates.flash
from queries import FILE_PATH
from utils.excel_processing import (
    find_cell_by_value,
    update_cell_by_value,
    get_value_by_location,
)
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dcc, ctx
import pandas as pd
from app import app


label = "Оприходование наклеек"

note = """
Тут можно внести наклейки на склад.
"""


def get_content() -> list:
    return [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label(
                                html.Span("Артикул*"),
                                className="period-title",
                            ),
                            dcc.Dropdown(
                                id="manager_input_sticker",
                                options=pd.read_excel(FILE_PATH)
                                .iloc[:, 11]
                                .dropna()
                                .fillna("")
                                .unique(),
                                value="",
                                multi=False,
                                placeholder="Выберите Наклейку",
                                searchable=True,
                                clearable=False,
                                style={"min-width": "520px", "display": "flex"},
                            ),
                        ],
                    ),
                    dbc.Col(
                        [
                            html.Label("Расход за весь период, шт.", style={}),
                            dbc.Input(
                                id="manager_input_sticker_expense_count",
                                disabled=True,
                                type="text",
                                value="",
                                style={"min-width": "100px", "display": "flex"},
                            ),
                        ],
                    ),
                    dbc.Col(
                        [
                            html.Label("На складе, шт.", style={}),
                            dbc.Input(
                                id="manager_input_sticker_storage",
                                disabled=True,
                                type="text",
                                value="",
                                style={"min-width": "100px", "display": "flex"},
                            ),
                        ],
                    ),
                    dbc.Col(
                        [
                            html.Label("Кол-во наклеек*", style={}),
                            dbc.Input(
                                id="manager_input_sticker_count",
                                type="text",
                                value="0",
                                style={"min-width": "100px", "display": "flex"},
                            ),
                        ],
                    ),
                    dbc.Col(
                        [
                            html.Label("Номер ячейки", style={}),
                            dbc.Input(
                                id="manager_input_sticker_cell",
                                type="text",
                                value="0",
                                style={"min-width": "100px", "display": "flex"},
                            ),
                        ],
                    ),
                    dbc.Col(
                        dbc.Button(
                            id="manager_add_sticker",
                            n_clicks=0,
                            children="Добавить",
                            style={"margin-top": "5px", "background-color": "#acd180"},
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        dbc.Button(
                            id="manager_remove_sticker",
                            n_clicks=0,
                            children="Убрать",
                            style={"margin-top": "5px", "background-color": "#fa0234"},
                        ),
                        width=4,
                    ),
                ]
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="save_new_storage_sticker"),
    ]


@app.callback(
    Output(component_id="save_new_storage_sticker", component_property="children"),
    Input(component_id="manager_add_sticker", component_property="n_clicks"),
    Input(component_id="manager_remove_sticker", component_property="n_clicks"),
    State(
        component_id="manager_input_sticker_expense_count", component_property="value"
    ),
    State(component_id="manager_input_sticker_storage", component_property="value"),
    State(component_id="manager_input_sticker", component_property="value"),
    State(component_id="manager_input_sticker_count", component_property="value"),
    State(component_id="manager_input_sticker_cell", component_property="value"),
    prevent_initial_call=True,
)
def update(  # noqa C901
    btn_add, btn_remove, expense_count, storage, sticker, count, cell
):
    if "" in {sticker, count}:
        return templates.flash.render("", "Необходимо заполнить все обязательные поля")

    location = find_cell_by_value(
        filename=FILE_PATH, search_value=sticker, number_column=11
    )

    if ctx.triggered_id == "manager_remove_sticker":
        expense_count = int(expense_count) + int(count)
        storage = int(storage) - int(count)
    else:
        storage = int(storage) + int(count)

    if count and (
        cell
        != get_value_by_location(FILE_PATH, row=location[0], column=location[1] + 3)
    ):
        values = [str(storage), str(expense_count), cell]
    else:
        values = [
            str(storage),
            str(expense_count),
            get_value_by_location(FILE_PATH, row=location[0], column=location[1] + 3),
        ]

    if update_cell_by_value(
        filename=FILE_PATH,
        row=location[0],
        columns=[location[1] + 1, location[1] + 2, location[1] + 3],
        values=values,
    ):
        return templates.flash.render(
            "",
            f"Количество для {sticker} было обновлено, "
            f"текущее количество - '{get_value_by_location(FILE_PATH, row=location[0], column=location[1] + 1)}',"
            f"ячейка - '{cell if cell else "Не указана"}'",
            color="#acd180" if ctx.triggered_id == "manager_add_sticker" else "#fa0234",
        )

    return templates.flash.render(
        "", "Произошла ошибка при обновлении данных", color="danger"
    )


@app.callback(
    Output(
        component_id="manager_input_sticker_expense_count", component_property="value"
    ),
    Output(component_id="manager_input_sticker_storage", component_property="value"),
    Output(component_id="manager_input_sticker_count", component_property="value"),
    Output(component_id="manager_input_sticker_cell", component_property="value"),
    Output(
        component_id="save_new_storage_sticker",
        component_property="children",
        allow_duplicate=True,
    ),
    Input(component_id="manager_input_sticker", component_property="value"),
    prevent_initial_call=True,
)
def get_value_to_cell(sticker):
    location = find_cell_by_value(
        filename=FILE_PATH, search_value=sticker, number_column=11
    )
    if location:
        return [
            get_value_by_location(FILE_PATH, row=location[0], column=location[1] + 2),
            get_value_by_location(FILE_PATH, row=location[0], column=location[1] + 1),
            0,
            get_value_by_location(FILE_PATH, row=location[0], column=location[1] + 3),
            None,
        ]
    return None, None, None, None, None
