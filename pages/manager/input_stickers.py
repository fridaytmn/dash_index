import templates.flash
from queries import FILE_PATH
from utils.excel_processing import find_cell_by_value, update_cell_by_value
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc
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
                        dcc.Dropdown(
                            id="manager_input_sticker",
                            options=pd.read_excel(FILE_PATH).iloc[:, 11].dropna().fillna("").unique(),
                            value="",
                            placeholder="Выберите Наклейку",
                            searchable=True,
                            clearable=False,
                        ),
                        width=40,
                    ),
                    dbc.Col(
                        dcc.Input(
                            id="manager_input_sticker_count",
                            type="text",
                            value="",
                        ),
                    ),
                    dbc.Col(
                        html.Button(
                            id="manager_save_input_sticker",
                            n_clicks=0,
                            children="Сохранить",
                        ),
                        width="auto",
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
    State(component_id="manager_input_sticker", component_property="value"),
    State(component_id="manager_input_sticker_count", component_property="value"),
    prevent_initial_call=True,
)
def update(_, sticker, count):
    if "" in {sticker, count}:
        return templates.flash.render("", "Необходимо заполнить все поля")

    location = find_cell_by_value(
        filename=FILE_PATH,
        search_value=sticker,
        number_column=11
    )

    if location:
        row, col = location
        print(f"Значение найдено в ячейке: строка {row}, столбец {col}")
    else:
        print("Значение не найдено.")

    if update_cell_by_value(
        filename=FILE_PATH,
        row=row,
        column=col+1,
        value=int(count)
    ):
        return templates.flash.render("", f"Количество для {sticker} было увеличино на {count}", color="#52F47E")

    return templates.flash.render("", f"Произошла ошибка при обновлении данных", color="danger")


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
