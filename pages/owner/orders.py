from queries.orders.owner import get_orders
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import html, dash_table
import utils.table_format
import pandas as pd
from app import app

label = "Список заявок"

note = """
В отчете отображается список заявок со всеми полями.
"""

allowed_roles = {"ADMIN"}


def get_content() -> list:
    return [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            id="get_orders",
                            n_clicks=0,
                            children="Показать",
                        ),
                        width=2,
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="orders"),
    ]


@app.callback(
    Output(component_id="orders", component_property="children"),
    Input("get_orders", "n_clicks"),
    prevent_initial_call=True,
)
def update(
    _,
):
    data = get_orders()
    data["id"] = data.index + 1
    # column_changes = {"username": "Логин", "name": "ФИО"}
    # data.rename(columns=column_changes, inplace=True)
    return get_table(data)


@table_wrapper()
def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="orders_table",
        columns=columns,
        style_cell_conditional=styles,
        page_size=50,
        sort_action="custom",
        sort_by=[],
        data=data.to_dict("records"),
    )
