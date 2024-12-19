from commands.orders.owner import create_new_customer
from queries.orders.owner import get_customers
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table
import utils.table_format
import templates.flash
import pandas as pd
from app import app
import logging

label = "Добавление и просмотр заказчиков"

note = """
Тут можно создать или просмотреть список заказчиков.
"""

allowed_roles = {"ADMIN", "OWNER"}


def get_content() -> list:
    return [
        html.H3(
            "Создание заказчика",
        ),
        html.Br(),
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Наименование организации*", style={}),
                            dbc.Input(
                                id="customers_naming",
                                type="text",
                                value="",
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("ИНН*", style={}),
                            dbc.Input(
                                id="customers_inn",
                                type="text",
                                value="",
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("e-mail адрес", style={}),
                            dbc.Input(
                                id="customers_email",
                                type="text",
                                value="",
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("Контактный номер", style={}),
                            dbc.Input(
                                id="customers_phone_number",
                                type="text",
                                value="",
                            ),
                        ],
                        width=2,
                    ),
                    dbc.Col(
                        dbc.Button(
                            id="create_customers",
                            n_clicks=0,
                            children="Добавить",
                        ),
                        width=2,
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="customers"),
        html.H3(
            "Список заказчиков",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            id="get_customers",
                            n_clicks=0,
                            children="Показать",
                        ),
                        width=2,
                    ),
                ],
            )
        ),
        html.Br(),
        html.Div(id="all_customers"),
    ]


@app.callback(
    Output(component_id="customers", component_property="children"),
    Input("create_customers", "n_clicks"),
    State(component_id="customers_naming", component_property="value"),
    State(component_id="customers_inn", component_property="value"),
    State(component_id="customers_email", component_property="value"),
    State(component_id="customers_phone_number", component_property="value"),
    prevent_initial_call=True,
)
def update_create_customers(_, customers_naming, customers_inn, customers_email, customers_phone_number):
    if "" in {customers_naming, customers_inn}:
        return templates.flash.render("", "Необходимо заполнить 'Название' и 'ИНН'")

    try:
        create_new_customer(customers_naming, customers_inn, customers_email, customers_phone_number)
    except Exception as error:
        logging.info(error)
        return templates.flash.render("", "Произошла ошибка при добавлении заказчика")

    return [
        html.Br(),
        dbc.Alert(f"Заказчик {customers_naming} был добавлен", color="warning"),
    ]


@app.callback(
    Output(component_id="all_customers", component_property="children"),
    Input(component_id="get_customers", component_property="n_clicks"),
    prevent_initial_call=True,
)
def update_all_customers(_):

    data = get_customers()

    column_changes = {
        "customers_id": "№",
        "customers_name": "Наименование",
        "customers_inn": "ИНН",
        "email": "Почта",
        "phone_number": "Контактный телефон",
    }

    data.rename(columns=column_changes, inplace=True)

    return get_table(data)


@table_wrapper()
def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="customers_table",
        columns=columns,
        style_cell_conditional=styles,
        page_size=50,
        sort_action="custom",
        sort_by=[],
        data=data.to_dict("records"),
    )
