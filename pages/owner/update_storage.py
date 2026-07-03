import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, dash_table
import pandas as pd
import base64
import io
import os

from utils.excel_processing import (
    normalize_article,
    merge_supplier_to_nomenclature,
    save_nomenclature_to_excel,
    export_nomenclature_to_store,
)
from utils.table_wrapper import table_wrapper
import utils.table_format
import templates.flash
from app import app

label = "Обновление склада"
allowed_roles = {"ADMIN", "OWNER"}

NOMENCLATURE_PATH = os.environ.get("NOMENCLATURE_PATH")
STORE_PATH = os.environ.get("STORE_PATH")


def get_content() -> list:
    """Возвращает layout для страницы обновления склада."""
    return [
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Upload(
                                id="upload_excel",
                                children=dbc.Button(
                                    "Загрузить файл поставщика (excel)",
                                    color="primary",
                                    id="upload_excel_btn",
                                ),
                                multiple=False,
                            ),
                            width="auto",
                        ),
                        dbc.Col(
                            dbc.Input(
                                id="supplier_name_input",
                                type="text",
                                placeholder="Введите название поставщика",
                                debounce=True,
                            ),
                            width=3,
                        ),
                    ]
                ),
            ],
            className="upload-wrapper",
        ),
        html.Br(),
        html.Div(id="merge_result", className="mb-2"),
        dash_table.DataTable(
            id="supplier_table",
            data=[],
            columns=[],
            row_deletable=True,
            editable=False,
            page_size=30,
            style_cell_conditional=[],
            style_table={"maxHeight": "600px", "overflowY": "auto"},
        ),
        html.Div(id="storage_update_result", className="mt-2"),
        dbc.Button(
            "Обновить Nomenclature",
            id="update_storage_button",
            color="success",
            className="mt-3",
            n_clicks=0,
        ),
        html.Br(),
        dbc.Button(
            "Перенос из Nomenclature в Store",
            id="update_nomenclature_to_storage_button",
            color="success",
            className="mt-3",
            n_clicks=0,
        ),
    ]


@table_wrapper()
def get_not_matched(data: pd.DataFrame):
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="not_matched_table",
        data=data.to_dict("records"),
        columns=[{"name": c, "id": c} for c in data.columns],
        style_cell_conditional=styles,
        page_size=20,
        sort_by=[],
        editable=False,
    )


@app.callback(
    Output("supplier_table", "data"),
    Output("supplier_table", "columns"),
    Output("supplier_table", "style_cell_conditional"),
    Output("merge_result", "children"),
    Output("upload_excel", "contents"),
    Input("upload_excel", "contents"),
    State("supplier_name_input", "value"),
    prevent_initial_call=True,
)
def upload_file(contents, supplier_name):  # noqa C901
    """
    Callback для загрузки Excel-файла поставщика и отображения таблицы для объединения.
    """

    if not contents:
        return [], [], [], "", None

    if not supplier_name:
        return (
            [],
            [],
            [],
            templates.flash.render("", "Необходимо заполнить поставщика"),
            None,
        )

    try:
        _, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        df = pd.read_excel(io.BytesIO(decoded))

        if df.empty:
            return (
                [],
                [],
                [],
                templates.flash.render("", "Файл пустой или некорректный"),
                None,
            )

        # Очистка артикула
        df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.strip().apply(normalize_article)

        # Добавляем поставщика
        df["Поставщик"] = supplier_name
        columns, styles = utils.table_format.generate(df)

        return (
            df.to_dict("records"),
            [{"name": c, "id": c} for c in df.columns],
            styles,
            "",
            None,
        )

    except Exception as e:
        return (
            [],
            [],
            [],
            templates.flash.render("", f"Ошибка загрузки Excel: {str(e)}"),
            None,
        )


@app.callback(
    Output("storage_update_result", "children"),
    Input("update_storage_button", "n_clicks"),
    State("supplier_table", "data"),
    State("supplier_name_input", "value"),
    prevent_initial_call=True,
)
def update_storage(_, table_rows, supplier_name):  # noqa C901
    """
    Callback для обновления склада на основе таблицы поставщика.
    """
    if not table_rows:
        return templates.flash.render("", "Нет данных в таблице")

    if not supplier_name:
        return templates.flash.render("", "Не указан поставщик")

    try:
        df_supplier = pd.DataFrame(table_rows)
        if df_supplier.empty:
            return templates.flash.render("", "Нет данных для обновления")

        try:
            df_nomenclature = pd.read_excel(NOMENCLATURE_PATH)
        except FileNotFoundError:
            return templates.flash.render("", "Файл номенклатуры не найден")
        except Exception as err:
            return templates.flash.render("", f"Ошибка чтения Excel: {str(err)}")

        if "Supplier_Designation" not in df_nomenclature.columns:
            return templates.flash.render(
                "", "В файле номенклатуры нет столбца 'Supplier_Designation'"
            )

        df_nomenclature["Supplier_Designation"] = (
            df_nomenclature["Supplier_Designation"]
            .astype(str)
            .str.strip()
            .apply(normalize_article)
        )

        try:
            updated_df, not_matched_df = merge_supplier_to_nomenclature(
                df_supplier, df_nomenclature, supplier_name
            )
        except Exception as err:
            return templates.flash.render("", f"Ошибка при объединении: {str(err)}")

        # Сохранение обратно в Excel с обработкой ошибок
        try:
            save_nomenclature_to_excel(updated_df, NOMENCLATURE_PATH)
        except Exception as err:
            return templates.flash.render("", f"Ошибка при сохранении: {str(err)}")

        # Если есть несовпавшие артикулы — вывести отдельную таблицу
        if not not_matched_df.empty:
            return html.Div(
                [
                    html.H4("Склад обновлён"),
                    html.Hr(),
                    html.H5("⚠ Несовпавшие артикулы"),
                    get_not_matched(not_matched_df),
                ]
            )

        return html.Div("Склад успешно обновлён (все позиции совпали)")

    except Exception as exc:
        return templates.flash.render("", f"Непредвидённая ошибка: {str(exc)}")


@app.callback(
    Output(
        "storage_update_result",
        "children",
        allow_duplicate=True,
    ),
    Input(
        "update_nomenclature_to_storage_button",
        "n_clicks",
    ),
    prevent_initial_call=True,
)
def update_store_from_nomenclature(_):

    try:

        rows = export_nomenclature_to_store(
            NOMENCLATURE_PATH,
            STORE_PATH,
        )

        return html.Div(f"Успешно перенесено {rows} строк.")

    except Exception as err:

        return templates.flash.render(
            "",
            f"Ошибка переноса: {err}",
        )
