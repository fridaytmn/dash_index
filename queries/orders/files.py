from utils.connectors.query_wraper import query
from queries.orders import connector


@query(connector)
def get_invoice_url(order_id: int) -> str:
    return f"""SELECT
    invoice_url as "Счет"
    FROM public.files
    WHERE order_id = {order_id}
"""
