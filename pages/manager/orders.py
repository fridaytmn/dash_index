from queries.orders.manager import get_orders
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc
import utils.table_format
import pandas as pd
from app import app
import utils.user

label = "Список всех заявок"

note = """
В отчете отображается список заявок для менеджера.
"""


def get_content() -> list:
    return [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            id="get_manager_orders",
                            n_clicks=0,
                            children="Показать",
                        ),
                        width=2,
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="manager_orders"),
    ]


@app.callback(
    Output(component_id="manager_orders", component_property="children"),
    Input("get_manager_orders", "n_clicks"),
    prevent_initial_call=True,
)
def update(
    _,
):
    data = get_orders()

    return get_table(data)


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
        editable=True,
    )
