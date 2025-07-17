import templates.flash
from queries import FILE_PATH
from utils.excel_processing import find_cell_by_value, update_cell_by_value, get_value_by_location
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc, callback_context
import utils.table_format
import pandas as pd
from app import app
import utils.user


label = "Оприходывание наклеек"

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
                                html.Span("Артикул"),
                                className="period-title",
                            ),
                            dcc.Dropdown(
                                id="manager_input_sticker",
                                options=pd.read_excel(FILE_PATH).iloc[:, 11].dropna().fillna("").unique(),
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
                            html.Label("Кол-во наклеек", style={}),
                            dbc.Input(
                                id="manager_input_sticker_count",
                                type="text",
                                value="",
                                style={"min-width": "120px", "display": "flex"},
                            ),
                        ],
                    ),
                    dbc.Col(
                        dbc.Button(
                            id="manager_save_input_sticker",
                            n_clicks=0,
                            children="Добавить",
                            style={"margin-top": "5px", "background-color": "#acd180"},
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        dbc.Button(
                            id="manager_save_remove_sticker",
                            n_clicks=0,
                            children="Убавить",
                            style={"margin-top": "5px", "background-color": "#f55151"},
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
    Input("manager_save_input_sticker", "n_clicks"),
    Input("manager_save_remove_sticker", "n_clicks"),
    State(component_id="manager_input_sticker", component_property="value"),
    State(component_id="manager_input_sticker_count", component_property="value"),
    prevent_initial_call=True,
)
def update(_, __, sticker, count):
    if "" in {sticker, count}:
        return templates.flash.render("", "Необходимо заполнить все поля")

    remove = callback_context.triggered[0]["prop_id"].split(".")[0] == "manager_save_remove_sticker"

    location = find_cell_by_value(filename=FILE_PATH, search_value=sticker, number_column=11)

    if location:
        row, col = location
        app.server.logger.info(f"Значение найдено в ячейке: строка {row}, столбец {col}")
    else:
        app.server.logger.info("Значение не найдено.")

    if update_cell_by_value(
        filename=FILE_PATH,
        row=row,
        column=col + 1,
        math_operation="-" if remove else "+",
        value=int(count),
    ):
        return templates.flash.render(
            "",
            f"Количество для {sticker} было {"уменьшино" if remove else "увеличино"} на {count}, "
            f"текущее количество '{get_value_by_location(FILE_PATH, row=location[0], column=location[1] + 1)}'",
            color=f"{"#f55151" if remove else "#acd180"}",
        )

    return templates.flash.render("", "Произошла ошибка при обновлении данных", color="danger")


@table_wrapper()
def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="manager_orders_table",
        columns=columns,
        style_cell_conditional=styles,
        page_size=50,
        sort_action="custom",
        sort_by=[],
        data=data.to_dict("records"),
    )
