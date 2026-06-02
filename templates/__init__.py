import urllib
import base64

url = "https://storage.yandexcloud.net/shvets-bucket-s3/intex/static/Logo.svg"
with urllib.request.urlopen(url) as response:
    LOGO_IMAGE = base64.b64encode(response.read()).decode()


INDEX_STRING = """<!DOCTYPE html>
<html>
    <head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""
