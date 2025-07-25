from utils.connectors.command_wraper import command
from queries.orders import connector


@command(connector)
def insert_file(order_id: int, invoice_filename: str, invoice_url: str) -> str:
    """Добавление файла (счет/фактура/спецификация) в БД"""
    return f"""INSERT INTO public.files (order_id, invoice_filename, invoice_url)
    VALUES ('{order_id}', '{invoice_filename}', '{invoice_url}')
"""
