from commands.order.owner import create_new_buyer
from queries.orders.owner import get_buyers
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table
import utils.table_format
import templates.flash
import pandas as pd
from app import app

label = "Заказчики"

note = """
Тут можно создать или просмотреть список заказчиков.
"""

allowed_roles = {"ADMIN"}


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
                            html.Label("Наименование заказчика*", style={}),
                            dbc.Input(
                                id="buyer_naming",
                                type="text",
                                value="",
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("ИНН заказчика*", style={}),
                            dbc.Input(
                                id="buyer_inn",
                                type="text",
                                value="",
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("Почтовый адрес", style={}),
                            dbc.Input(
                                id="buyer_email",
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
                                id="buyer_phone_number",
                                type="text",
                                value="",
                            ),
                        ],
                        width=2,
                    ),
                    dbc.Col(
                        dbc.Button(
                            id="create_buyer",
                            n_clicks=0,
                            children="Добавить",
                        ),
                        width=2,
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="buyer"),
        html.H3(
            "Список заказчиков",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            id="get_buyers",
                            n_clicks=0,
                            children="Показать",
                        ),
                        width=2,
                    ),
                ],
            )
        ),
        html.Br(),
        html.Div(id="all_buyer"),
    ]


@app.callback(
    Output(component_id="buyer", component_property="children"),
    Input("create_buyer", "n_clicks"),
    State(component_id="buyer_naming", component_property="value"),
    State(component_id="buyer_inn", component_property="value"),
    State(component_id="buyer_email", component_property="value"),
    State(component_id="buyer_phone_number", component_property="value"),
    prevent_initial_call=True,
)
def update_create_buyer(
    _, buyer_naming, buyer_inn, buyer_email, buyer_phone_number
):
    if None in {buyer_naming, buyer_inn}:
        return templates.flash.render("", "Необходимо заполнить 'Название' и 'ИНН'")

    try:
        create_new_buyer(buyer_naming, buyer_inn, buyer_email, buyer_phone_number)
    except Exception as error:
        print(error)

    return [
        html.Br(),
        dbc.Alert(f"Заказчик {buyer_naming} был добавлен", color="warning"),
    ]

@app.callback(
    Output(component_id="all_buyer", component_property="children"),
    Input(component_id="get_buyers", component_property="n_clicks"),
    prevent_initial_call=True,
)
def update_all_buyer(_):

    data = get_buyers()

    column_changes = {"buyer_id": "№",
                      "buyer_name": "Наименование",
                      "buyer_inn": "ИНН",
                      "email": "Почта",
                      "phone_number": "Контактный телефон",
                      }

    data.rename(columns=column_changes, inplace=True)

    return get_table(data)

@table_wrapper()
def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="buyer_table",
        columns=columns,
        style_cell_conditional=styles,
        page_size=50,
        sort_action="custom",
        sort_by=[],
        data=data.to_dict("records"),
    )
