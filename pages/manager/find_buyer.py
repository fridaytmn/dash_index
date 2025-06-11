from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table
import pandas as pd

from utils.table_wrapper import table_wrapper
import utils.table_format
import templates.flash
from app import app
import utils.user

label = "Поиск по Покупателю"

note = """
В отчете отображается склад по Покупателю.
"""


def get_content() -> list:
    return [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Покупатель", style={}),
                            dbc.Input(
                                id="manager_find_buyer_input",
                                type="text",
                                value="",
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Button(
                            id="get_find_buyer",
                            n_clicks=0,
                            children="Найти",
                        ),
                        width="auto",
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="find_buyer_manager"),
    ]


@app.callback(
    Output("find_buyer_manager", "children"),
    Input("get_find_buyer", "n_clicks"),
    State("manager_find_buyer_input", "value"),
    prevent_initial_call=True,
)
def update(_, buyer):
    if buyer == "":
        return templates.flash.render("", "Необходимо заполнить все поля")
    data = pd.read_excel("C:\\files\\reestr\\Nomenclature.xlsx")
    data = data.fillna("")[data.fillna("")["Покупатель"].str.contains(buyer)]
    result = data.drop(data.columns[[0, 1, 2, 3, 4, -1]], axis=1)
    return get_table(result)


@table_wrapper()
def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="manager_find_buyer",
        columns=columns,
        style_cell_conditional=styles,
        page_size=100,
        sort_action="custom",
        sort_by=[],
        data=data.to_dict("records"),
        editable=False,
        cell_selectable=False,
    )
