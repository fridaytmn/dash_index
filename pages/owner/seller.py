import logging

from queries.orders.owner import get_sellers
from commands.orders.owner import create_new_seller, update_seller, delete_seller
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table, no_update
import utils.table_format
import templates.flash
import pandas as pd
from app import app

label = "Поставщики"

note = """
Создание, просмотр, изменение и удаление поставщиков (таблица sellers).
Для редактирования укажите № из списка и новые данные.
"""

allowed_roles = {"ADMIN", "OWNER"}


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
        html.H3("Редактирование и удаление поставщика"),
        html.Br(),
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("№ поставщика*", style={}),
                            dbc.Input(
                                id="edit_seller_id",
                                type="number",
                                min=1,
                                value="",
                            ),
                        ],
                        width=2,
                    ),
                    dbc.Col(
                        [
                            html.Label("Наименование поставщика*", style={}),
                            dbc.Input(
                                id="edit_seller_naming",
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
                                id="edit_seller_inn",
                                type="text",
                                value="",
                            ),
                        ],
                        width=2,
                    ),
                    dbc.Col(
                        [
                            html.Label("Почтовый адрес", style={}),
                            dbc.Input(
                                id="edit_seller_email",
                                type="text",
                                value="",
                            ),
                        ],
                        width=2,
                    ),
                    dbc.Col(
                        [
                            html.Label("Контактный номер", style={}),
                            dbc.Input(
                                id="edit_seller_phone_number",
                                type="text",
                                value="",
                            ),
                        ],
                        width=2,
                    ),
                    dbc.Col(
                        dbc.Button(
                            id="update_seller",
                            n_clicks=0,
                            children="Сохранить",
                            color="primary",
                        ),
                        width=1,
                        className="d-flex align-items-end",
                        style={"margin-top": "20px"},
                    ),
                    dbc.Col(
                        dbc.Button(
                            id="delete_seller",
                            n_clicks=0,
                            children="Удалить",
                            color="danger",
                        ),
                        width=1,
                        className="d-flex align-items-end",
                        style={"margin-left": "20px", "margin-top": "20px"},
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="seller_edit"),
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
    if "" in {seller_naming, seller_inn}:
        return templates.flash.render("", "Необходимо заполнить 'Название' и 'ИНН'")

    try:
        create_new_seller(seller_naming, seller_inn, seller_email, seller_phone_number)
    except Exception as error:
        logging.info(error)
        return templates.flash.render("", "Произошла ошибка при добавлении поставщика")
    return [
        html.Br(),
        dbc.Alert(f"Поставщик {seller_naming} был добавлен", color="warning"),
    ]


def _sellers_table():
    data = get_sellers()
    column_changes = {
        "seller_id": "№",
        "seller_name": "Наименование",
        "seller_inn": "ИНН",
        "email": "Почта",
        "phone_number": "Контактный телефон",
    }
    data.rename(columns=column_changes, inplace=True)
    return get_table(data)


@app.callback(
    Output(component_id="seller_edit", component_property="children"),
    Output(
        component_id="all_seller", component_property="children", allow_duplicate=True
    ),
    Input("update_seller", "n_clicks"),
    State(component_id="edit_seller_id", component_property="value"),
    State(component_id="edit_seller_naming", component_property="value"),
    State(component_id="edit_seller_inn", component_property="value"),
    State(component_id="edit_seller_email", component_property="value"),
    State(component_id="edit_seller_phone_number", component_property="value"),
    prevent_initial_call=True,
)
def update_existing_seller(  # noqa C901
    _,
    seller_id,
    seller_naming,
    seller_inn,
    seller_email,
    seller_phone_number,
):
    if seller_id is None or seller_id == "":
        return templates.flash.render("", "Укажите № поставщика"), no_update
    if "" in {seller_naming, seller_inn}:
        return (
            templates.flash.render("", "Необходимо заполнить 'Название' и 'ИНН'"),
            no_update,
        )

    try:
        update_seller(
            int(seller_id),
            seller_naming,
            seller_inn,
            seller_email,
            seller_phone_number,
        )
    except Exception as error:
        logging.info(error)
        return (
            templates.flash.render("", "Произошла ошибка при изменении поставщика"),
            no_update,
        )

    return [
        html.Br(),
        dbc.Alert(
            f"Поставщик №{seller_id} ({seller_naming}) обновлён",
            color="success",
        ),
    ], _sellers_table()


@app.callback(
    Output(
        component_id="seller_edit", component_property="children", allow_duplicate=True
    ),
    Output(
        component_id="all_seller", component_property="children", allow_duplicate=True
    ),
    Input("delete_seller", "n_clicks"),
    State(component_id="edit_seller_id", component_property="value"),
    prevent_initial_call=True,
)
def remove_seller(_, seller_id):
    if seller_id is None or seller_id == "":
        return (
            templates.flash.render("", "Укажите № поставщика для удаления"),
            no_update,
        )

    try:
        delete_seller(int(seller_id))
    except Exception as error:
        logging.info(error)
        return (
            templates.flash.render("", "Произошла ошибка при удалении поставщика"),
            no_update,
        )

    return [
        html.Br(),
        dbc.Alert(f"Поставщик №{seller_id} удалён", color="warning"),
    ], _sellers_table()


@app.callback(
    Output(component_id="all_seller", component_property="children"),
    Input(component_id="get_sellers", component_property="n_clicks"),
    prevent_initial_call=True,
)
def update_all_seller(_):
    return _sellers_table()


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
