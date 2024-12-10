from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import dash_table, html, ctx, dcc
import utils.table_format
import pandas as pd
from app import app

label = "Редактируемая таблица"

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
                            id="get_edit_table",
                            n_clicks=0,
                            children="Показать",
                        ),
                        width=2,
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="edit_table"),
    ]


@app.callback(
    Output("edit_table", "children"),
    Input("get_edit_table", "n_clicks"),
    prevent_initial_call=True,
)
def update(_):

    product_data = {
        "product": ["apples", "bananas", "milk", "eggs", "bread", "cookies"],
        "price": [3.75, 1.65, 1.55, 3.60, 3.00, 3.97],
        "unit": ["kg", "kg", "l", "dz", "ea", "pkg"],
    }

    df_product = pd.DataFrame(product_data)

    return [
        dcc.Store("notification_settings_sent_store", data=df_product.to_dict("records")),
        html.Div(id="notification_settings_tabs_content"),
        dbc.Button(id="add-btn", n_clicks=0, children="Добавить строку"),
    ]


@app.callback(
    Output("notification_settings_tabs_content", "children"),
    Input("add-btn", "n_clicks"),
    Input("notification_settings_sent_store", "data"),
)
def add_row(button, data) -> list:

    data_new = pd.DataFrame(data)

    new_order_line = {"product": "", "price": 0, "unit": "", "quantity": 0, "total": 0}
    df_new_order_line = pd.DataFrame(new_order_line, index=[0])

    data_new_2 = pd.DataFrame()

    if ctx.triggered_id == "add-btn":
        data_new_2 = pd.concat([data_new_2, data_new], ignore_index=True)
        data_added_row = pd.concat([data_new_2, df_new_order_line], ignore_index=True)
        data_new = data_added_row
    else:
        data_added_row = data_new

    return [
        html.Label("kek"),
        get_table(data_added_row),
    ]


def get_data():

    product_data = {
        "product": ["apples", "bananas", "milk", "eggs", "bread", "cookies"],
        "price": [3.75, 1.65, 1.55, 3.60, 3.00, 3.97],
        "unit": ["kg", "kg", "l", "dz", "ea", "pkg"],
    }

    df_product = pd.DataFrame(product_data)

    return df_product


@table_wrapper()
def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="1234",
        columns=columns,
        style_cell_conditional=styles,
        page_size=50,
        sort_action="custom",
        sort_by=[],
        data=data.to_dict("records"),
        row_deletable=True,
    )
