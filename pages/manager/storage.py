from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table
import pandas as pd

from utils.table_wrapper import table_wrapper
import utils.table_format
import templates.flash
from app import app
import utils.user

label = "Складские остатки"

note = """
В отчете отображается складские остатки.
"""


def get_content() -> list:
    return [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            id="get_storage",
                            n_clicks=0,
                            children="Показать остатки",
                        ),
                        width=2,
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="storage_manager"),
    ]


@app.callback(
    Output("storage_manager", "children"),
    Input("get_storage", "n_clicks"),
    prevent_initial_call=True,
)
def update(_):
    data = pd.read_excel("C:\\files\\reestr\\Nomenclature.xlsx")
    result = data.iloc[:, [5, 6, 8, 9]].dropna(subset=["Склад Мск, шт.", "Склад Тмн, шт."], how="all").fillna(0)
    result["Итого"] = result["Склад Мск, шт."] + result["Склад Тмн, шт."]
    return get_table(result)


@table_wrapper()
def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="manager_storage",
        columns=columns,
        style_cell_conditional=styles,
        page_size=100,
        sort_action="custom",
        sort_by=[],
        data=data.to_dict("records"),
        editable=False,
        cell_selectable=False,
    )
