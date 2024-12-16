from queries.orders.manager import get_orders, get_orders_by_buyer
from queries.orders.owner import get_buyers
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc
import utils.table_format
import pandas as pd
from app import app
import utils.user
from pages import OPTION_ALL

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
                        [
                            html.Label("Заказчик", style={}),
                            dcc.Dropdown(
                                id="manager_buyer_orders",
                                options=[
                                    {
                                        "label": f'{row["buyer_name"]} {row["buyer_inn"]}',
                                        "value": row["buyer_name"] + " " + row["buyer_inn"]
                                    }
                                    for index, row in get_buyers().iterrows()
                                ],
                                searchable=True,
                                placeholder=OPTION_ALL,
                                style={"min-width": "320px", "min-height": "40px"},
                                value=OPTION_ALL,
                            ),
                        ],
                        width=3,
                    ),
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
    State(component_id="manager_buyer_orders", component_property="value"),
    prevent_initial_call=True,
)
def update(
    _, buyer
):
    if buyer is None:
        return get_table(get_orders())
    return get_table(get_orders_by_buyer(buyer))


@table_wrapper()
def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="manager_orders_table",
        columns=columns,
        style_cell_conditional=styles,
        page_size=100,
        sort_action="custom",
        sort_by=[],
        data=data.to_dict("records"),
        editable=True,
    )
