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
def get_customers():
    return """SELECT DISTINCT
    name,
    tax_id
    FROM intex_test.customers
    GROUP BY name, tax_id"""


@query(connector)
def get_sellers():
    return """SELECT
    *
    FROM public.sellers"""
