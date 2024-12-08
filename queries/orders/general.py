from utils.connectors.query_wraper import query
from queries.orders import connector


@query(connector)
def get_last_number_order():
    return """SELECT id FROM public.orders ORDER BY id DESC LIMIT 1"""
