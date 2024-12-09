from commands.order.owner import create_new_buyer
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table
import utils.table_format
import templates.flash
import pandas as pd
from app import app

label = "Создание заказчика"

note = """
Тут можно создать заказчика.
"""

allowed_roles = {"ADMIN"}


def get_content() -> list:
    return [
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
                            children="Сохранить",
                        ),
                        width=2,
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="buyer"),
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
def update(
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

#
# @table_wrapper()
# def get_table(data: pd.DataFrame) -> dash_table.DataTable:
#     columns, styles = utils.table_format.generate(data)
#     return dash_table.DataTable(
#         id="buyer_table",
#         columns=columns,
#         style_cell_conditional=styles,
#         page_size=50,
#         sort_action="custom",
#         sort_by=[],
#         data=data.to_dict("records"),
#     )
