from dash.dependencies import Input, Output, State
from commands.orders.files import insert_file
from utils.connectors.s3 import s3_client
from dash import dcc, html
import base64
from app import app


label = "Загрузка файла"

note = """
Загрузка файла.
"""

BUCKET_NAME = "mobile-apps"


def get_content() -> list:
    return [
        html.Div(
            [
                html.H1("Загрузка PDF в MinIO"),
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(["Перетащите файл или ", html.A("выберите файл")]),
                    style={
                        "width": "100%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                        "margin": "10px",
                    },
                    multiple=False,  # Поддержка только одного файла за раз
                ),
                html.Div(id="output-data-upload"),
            ]
        )
    ]


@app.callback(
    Output("output-data-upload", "children"), Input("upload-data", "contents"), State("upload-data", "filename")
)
def upload_to_s3(contents, filename):
    if contents is not None:
        # Извлечение содержимого файла
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)

        # Загрузка в MinIO
        try:
            s3_client.put_object(Bucket=BUCKET_NAME, Key=filename, Body=decoded, ContentType="application/pdf")

            # Генерация ссылки на скачивание (постоянная или временная)
            file_url = s3_client.generate_presigned_url(
                "get_object", Params={"Bucket": BUCKET_NAME, "Key": filename}, ExpiresIn=2678400
            )

            # Сохранение в базу данных
            try:
                insert_file(1, filename, file_url)
            except Exception as e:
                print(e)

            # Возврат ссылки пользователю
            return html.Div(
                [
                    html.P(f"Файл '{filename}' успешно загружен в MinIO."),
                    html.P(f"Ссылка на файл:"),
                    html.A(file_url, href=file_url, target="_blank"),
                ]
            )
        except Exception as e:
            return html.Div(f"Ошибка при загрузке: {str(e)}")
    return html.Div("Не удалось загрузить файл.")
