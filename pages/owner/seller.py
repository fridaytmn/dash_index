from queries.orders.owner import get_sellers
from commands.orders.owner import create_new_seller
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table
import utils.table_format
import templates.flash
import pandas as pd
from app import app

label = "Поставщики"

note = """
Тут можно создать или просмотреть список поставщиков.
"""

allowed_roles = {"ADMIN"}


def get_content() -> list:
    return [
        html.H3(
            "Создание поставщика",
        ),
        html.Br(),
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Наименование поставщика*", style={}),
                            dbc.Input(
                                id="seller_naming",
                                type="text",
                                value="",
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("ИНН/счет поставщика*", style={}),
                            dbc.Input(
                                id="seller_inn",
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
                                id="seller_email",
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
                                id="seller_phone_number",
                                type="text",
                                value="",
                            ),
                        ],
                        width=2,
                    ),
                    dbc.Col(
                        dbc.Button(
                            id="create_seller",
                            n_clicks=0,
                            children="Добавить",
                        ),
                        width=2,
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="seller"),
        html.H3(
            "Список поставщиков",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            id="get_sellers",
                            n_clicks=0,
                            children="Показать",
                        ),
                        width=2,
                    ),
                ],
            )
        ),
        html.Br(),
        html.Div(id="all_seller"),
    ]


@app.callback(
    Output(component_id="seller", component_property="children"),
    Input("create_seller", "n_clicks"),
    State(component_id="seller_naming", component_property="value"),
    State(component_id="seller_inn", component_property="value"),
    State(component_id="seller_email", component_property="value"),
    State(component_id="seller_phone_number", component_property="value"),
    prevent_initial_call=True,
)
def update_create_seller(
    _, seller_naming, seller_inn, seller_email, seller_phone_number
):
    if None in {seller_naming, seller_inn}:
        return templates.flash.render("", "Необходимо заполнить 'Название' и 'ИНН'")

    try:
        create_new_seller(seller_naming, seller_inn, seller_email, seller_phone_number)
    except Exception as error:
        print(error)

    return [
        html.Br(),
        dbc.Alert(f"Поставщик {seller_naming} был добавлен", color="warning"),
    ]

@app.callback(
    Output(component_id="all_seller", component_property="children"),
    Input(component_id="get_sellers", component_property="n_clicks"),
    prevent_initial_call=True,
)
def update_all_seller(_):

    data = get_sellers()

    column_changes = {"seller_id": "№",
                      "seller_name": "Наименование",
                      "seller_inn": "ИНН",
                      "email": "Почта",
                      "phone_number": "Контактный телефон",
                      }

    data.rename(columns=column_changes, inplace=True)

    return get_table(data)


@table_wrapper()
def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="seller_table",
        columns=columns,
        style_cell_conditional=styles,
        page_size=50,
        sort_action="custom",
        sort_by=[],
        data=data.to_dict("records"),
    )
