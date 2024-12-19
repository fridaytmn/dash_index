from utils.connectors.query_wraper import query
from queries.orders import connector


@query(connector)
def get_orders():
    return """SELECT
    id AS "Номер заявки",
    seller AS "Поставщик"
    FROM public.orders
    ORDER BY id"""


@query(connector)
def get_buyers():
    return """SELECT DISTINCT
    buyer_name,
    buyer_inn
    FROM public.buyer
    GROUP BY buyer_name, buyer_inn"""


@query(connector)
def get_sellers():
    return """SELECT
    *
    FROM public.sellers"""
