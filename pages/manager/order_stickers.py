import templates.flash
from queries import FILE_PATH
from utils.excel_processing import (
    find_cell_by_value,
    update_cell_by_value,
    get_value_by_location,
)
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc
import utils.table_format
import pandas as pd
from app import app
import utils.user


label = "Заказ наклеек"

note = """
Тут можно заказать наклейки на склад.
"""


def get_content() -> list:
    return [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label(
                                html.Span("Наименование"),
                                className="period-title",
                            ),
                            dcc.Dropdown(
                                id="manager_order_sticker",
                                options=pd.read_excel(FILE_PATH)
                                .iloc[:, 11]
                                .dropna()
                                .fillna("")
                                .unique(),
                                value="",
                                placeholder="Выберите Наклейку",
                                searchable=True,
                                clearable=False,
                                multi=True,
                                style={
                                    "min-width": "520px",
                                    "width": "520px",
                                    "min-height": "300px",
                                    "display": "flex",
                                },
                            ),
                        ],
                    ),
                    dbc.Col(
                        [
                            html.Label("Кол-во наклеек*", style={}),
                            dbc.Input(
                                id="manager_order_sticker_count",
                                type="text",
                                value="",
                                style={"min-width": "120px", "display": "flex"},
                            ),
                        ],
                    ),
                    dbc.Col(
                        [
                            html.Label("Номер ячейки", style={}),
                            dbc.Input(
                                id="manager_order_sticker_cell",
                                type="text",
                                value="",
                                style={"min-width": "120px", "display": "flex"},
                            ),
                        ],
                    ),
                    dbc.Col(
                        dbc.Button(
                            id="manager_update_sticker",
                            n_clicks=0,
                            children="Обновить",
                            style={"margin-top": "5px", "background-color": "#acd180"},
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
    Output(component_id="save_order_sticker", component_property="children"),
    Input(component_id="manager_create_order_sticker", component_property="n_clicks"),
    State(component_id="manager_order_sticker", component_property="value"),
    State(component_id="manager_order_sticker_count", component_property="value"),
    State(component_id="manager_order_sticker_cell", component_property="value"),
    prevent_initial_call=True,
)
def update(_, sticker, count, cell):
    if "" in {sticker, count}:
        return templates.flash.render("", "Необходимо заполнить все обязательные поля")

    location = find_cell_by_value(
        filename=FILE_PATH, search_value=sticker, number_column=11
    )

    if count and (
        cell
        != get_value_by_location(FILE_PATH, row=location[0], column=location[1] + 2)
    ):
        values = [str(count), cell]
    else:
        values = [
            str(count),
            get_value_by_location(FILE_PATH, row=location[0], column=location[1] + 2),
        ]

    if update_cell_by_value(
        filename=FILE_PATH,
        row=location[0],
        columns=[location[1] + 1, location[1] + 2],
        values=values,
    ):
        return templates.flash.render(
            "",
            f"Количество для {sticker} было обновлено, "
            f"текущее количество - '{count}', ячейка - '{cell if cell else "Не указана"}'",
            color="#acd180",
        )

    return templates.flash.render(
        "", "Произошла ошибка при обновлении данных", color="danger"
    )


@table_wrapper()
def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="manager_new_orders_table",
        columns=columns,
        style_cell_conditional=styles,
        page_size=50,
        sort_action="custom",
        sort_by=[],
        data=data.to_dict("records"),
    )


@app.callback(
    Output(component_id="manager_order_sticker_count", component_property="value"),
    Output(component_id="manager_order_sticker_cell", component_property="value"),
    Output(
        component_id="save_new_order_sticker",
        component_property="children",
        allow_duplicate=True,
    ),
    Input(component_id="manager_order_sticker", component_property="value"),
    prevent_initial_call=True,
)
def get_value_to_cell(sticker):
    location = find_cell_by_value(
        filename=FILE_PATH, search_value=sticker, number_column=11
    )
    if location:
        return [
            get_value_by_location(FILE_PATH, row=location[0], column=location[1] + 1),
            get_value_by_location(FILE_PATH, row=location[0], column=location[1] + 2),
            [],
        ]
    return None, None, None
