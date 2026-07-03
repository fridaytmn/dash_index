from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import html, dash_table
import pandas as pd
import os

from utils.table_wrapper import table_wrapper
import utils.table_format
from app import app
import utils.user

label = "Складские остатки"

note = """
В отчете отображается складские остатки.
"""

STORE_PATH = os.environ.get("STORE_PATH")


def get_content() -> list:
    return [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            id="get_storage",
                            n_clicks=0,
                            children="Показать остатки",
                            style={"min-width": "160px"},
                        ),
                        width=3,
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="storage_manager"),
    ]


@app.callback(
    Output("storage_manager", "children"),
    Input("get_storage", "n_clicks"),
    prevent_initial_call=True,
)
def update(_):
    data = pd.read_excel(STORE_PATH)
    return get_table(data)


@table_wrapper()
def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="manager_storage",
        columns=columns,
        style_cell_conditional=styles,
        page_size=100,
        sort_action="custom",
        sort_by=[],
        data=data.to_dict("records"),
        editable=False,
        cell_selectable=False,
    )
