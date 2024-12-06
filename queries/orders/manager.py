from utils.connectors.query_wraper import query
from queries.orders import connector


@query(connector)
def get_orders():
    return """SELECT
    article,
    product_name,
    product_naming,
    brand,
    quantity_ordered,
    quantity,
    unit,
    buyer
    FROM public.orders"""
