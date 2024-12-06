from utils.connectors.query_wraper import query
from queries.orders import connector


@query(connector)
def get_orders():
    return """SELECT
    *
    FROM public.orders"""
