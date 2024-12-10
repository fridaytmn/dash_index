import commands.orders.save_order
import queries.orders.general
import templates.flash
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table
import utils.table_format
import pandas as pd
from app import app
import utils.user
import logging

label = "Регистрация новой заявки"

note = """
Тут можно создать новую заявку.
"""


def get_content() -> list:
    return [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Артикул", style={}),
                            dbc.Input(
                                id="manager_article_new_order",
                                type="text",
                                value="",
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("Наименование", style={}),
                            dbc.Input(
                                id="manager_naming_new_order",
                                type="text",
                                value="",
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("Бренд", style={}),
                            dbc.Input(
                                id="manager_brand_new_order",
                                type="text",
                                value="",
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        [
                            html.Label("Заказанное количество", style={}),
                            dbc.Input(
                                id="manager_ordered_count_new_order",
                                type="number",
                                value="1",
                            ),
                        ],
                        width=2,
                    ),
                    dbc.Col(
                        [
                            html.Label("Количество", style={}),
                            dbc.Input(
                                id="manager_count_new_order",
                                type="number",
                                value="1",
                            ),
                        ],
                        width=2,
                    ),
                    dbc.Col(
                        [
                            html.Label("Ед. изм.", style={}),
                            dbc.Select(
                                id="manager_ed_izm_new_order",
                                options=[
                                    {
                                        "label": "Шт.",
                                        "value": 2,
                                    },
                                    {
                                        "label": "л.",
                                        "value": 1,
                                    },
                                    {
                                        "label": "Иное",
                                        "value": 0,
                                    },
                                ],
                                value=1,
                            ),
                        ],
                        width=2,
                    ),
                    dbc.Col(
                        [
                            html.Label("Покупатель", style={}),
                            dbc.Input(
                                id="manager_buyer_new_order",
                                type="text",
                                value="",
                            ),
                        ],
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Button(
                            id="manager_save_new_order",
                            n_clicks=0,
                            children="Сохранить",
                        ),
                        width="auto",
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="save_new_order_from_manager"),
    ]


@app.callback(
    Output(component_id="save_new_order_from_manager", component_property="children"),
    Input("manager_save_new_order", "n_clicks"),
    State(component_id="manager_article_new_order", component_property="value"),
    State(component_id="manager_naming_new_order", component_property="value"),
    State(component_id="manager_brand_new_order", component_property="value"),
    State(component_id="manager_ordered_count_new_order", component_property="value"),
    State(component_id="manager_count_new_order", component_property="value"),
    State(component_id="manager_ed_izm_new_order", component_property="value"),
    State(component_id="manager_buyer_new_order", component_property="value"),
    prevent_initial_call=True,
)
def update(_, article, product_name, brand, quanity_ordered, quantity, unit, buyer):
    if "" in {article, product_name, brand, quanity_ordered, quantity, unit, buyer}:
        return templates.flash.render("", "Необходимо заполнить все поля")
    number_id = queries.orders.general.get_last_number_order()
    try:
        commands.order.save_order.create_new_order(article, product_name, brand, quanity_ordered, quantity, unit, buyer)
    except Exception as error:
        logging.info(error)
        return templates.flash.render("", "Что-то пошло не по плану")

    product_data = {
        "id": [number_id["id"][0]],
        "article": [article],
        "name": [product_name],
        "brand": [brand],
        "ordered_count": [quanity_ordered],
        "count": [quantity],
        "ed_izm": [unit],
        "buyer": [buyer],
    }

    data = pd.DataFrame(product_data)

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
    )
