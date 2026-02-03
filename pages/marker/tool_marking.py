from queries import FILE_PATH
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dash_table, _dash_renderer
import utils.table_format
import pandas as pd
from app import app
import dash_mantine_components as dmc

_dash_renderer._set_react_version("18.2.0")

label = "Маркировка инструмента"
allowed_roles = {"ADMIN"}


def get_content() -> list:
    sticker_list = pd.read_excel(FILE_PATH).iloc[:, 1].dropna().astype(str).unique()

    return [
        dmc.MantineProvider(
            children=[
                html.Div(
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("Артикул поставщика"),
                                    dmc.Select(
                                        id="tool_marking_article",
                                        data=sticker_list,
                                        placeholder="Артикул",
                                        searchable=True,
                                        clearable=True,
                                        w="450px",
                                    ),
                                ]
                            ),
                            dbc.Col(
                                dbc.Button(
                                    "Показать",
                                    id="get_tool_marking_search_marking",
                                    style={
                                        "margin-top": "5px",
                                        "background-color": "#acd180",
                                        "min-width": "170px",
                                    },
                                ),
                                width="auto",
                            ),
                        ],
                        align="end",
                    ),
                    className="form-inline-wrapper",
                ),
                html.Div(id="tool_marking_text_mark"),
            ]
        )
    ]


@app.callback(
    Output("tool_marking_text_mark", "children"),
    Input("get_tool_marking_search_marking", "n_clicks"),
    State("tool_marking_article", "value"),
    prevent_initial_call=True,
)
def fill_expense(_, article):
    if not article:
        return ""

    data = pd.read_excel("C:\\files\\reestr\\Nomenclature.xlsx")
    data = data.fillna("")[
        data.fillna("")[
            "Артикул                               (Поставщик)"
        ].str.contains(article)
    ]
    result = data.iloc[:, [1, 2, 5, 16]]

    return get_table(result)


def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="tool_marking_table",
        style_cell={
            "whiteSpace": "nowrap",
            "padding": "6px",
        },
        editable=True,
        columns=columns,
        page_size=10,
        sort_action="custom",
        sort_by=[],
        data=data.to_dict("records"),
        style_cell_conditional=styles,
    )
