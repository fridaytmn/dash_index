import templates.flash
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table, dcc
import utils.table_format
import pandas as pd
from app import app
import utils.user

label = "Оприходывание наклеек"

note = """
Тут можно внести наклейки на склад.
"""

is_hidden = True


def get_content() -> list:
    return [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Dropdown(
                            id="manager_input_sticker",
                            options=[],
                            # options=pd.read_excel("C:\\files\\reestr\\Nomenclature.xlsx").iloc[:, 10].dropna().fillna("").unique(),
                            value="",
                            placeholder="Выберите Наклейку",
                            searchable=True,
                            clearable=False,
                        ),
                        width="8",
                    ),
                    dbc.Col(
                        dcc.Input(
                            id="manager_input_sticker_count",
                            type="text",
                            value="",
                        ),
                        width="2",
                    ),
                    dbc.Col(
                        html.Button(
                            id="manager_save_input_sticker",
                            n_clicks=0,
                            children="Сохранить",
                        ),
                        width="auto",
                    ),
                ]
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="save_new_storage_sticker"),
    ]


@app.callback(
    Output(component_id="save_new_storage_sticker", component_property="children"),
    Input("manager_save_input_sticker", "n_clicks"),
    State(component_id="manager_input_sticker", component_property="value"),
    prevent_initial_call=True,
)
def update(_, sticker):
    if "" in {sticker}:
        return templates.flash.render("", "Необходимо заполнить все поля")
    # order_id = queries.orders.general.get_last_number_order()
    # try:
    #     save_order.create_new_order(article, product_name, brand, quanity_ordered, quantity, unit, customer)
    #     owner.insert_new_order(order_id["id"][0])
    # except Exception as error:
    #     logging.info(error)
    #     return templates.flash.render("", "Что-то пошло не по плану")
    #
    # product_data = {
    #     "id": [order_id["id"][0]],
    #     "article": [article],
    #     "name": [product_name],
    #     "brand": [brand],
    #     "ordered_count": [quanity_ordered],
    #     "count": [quantity],
    #     "ed_izm": [unit],
    #     "customer": [customer],
    # }
    #
    # data = pd.DataFrame(product_data)
    #
    # return get_table(data)


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
