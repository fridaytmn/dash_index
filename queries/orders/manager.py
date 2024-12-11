from utils.connectors.query_wraper import query
from queries.orders import connector


@query(connector)
def get_orders():
    return f"""SELECT
    id,
    article,
    product_name,
    product_naming,
    brand,
    quantity_ordered,
    quantity,
    unit,
    buyer,
    invoice
    FROM public.orders
    ORDER BY id
"""
