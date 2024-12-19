from utils.connectors.query_wraper import query
from queries.orders import connector


@query(connector)
def get_orders_by_customer(buyer: str):
    return f"""SELECT
    po.id,
    po.article,
    po.product_name,
    po.product_naming,
    po.brand,
    po.quantity_ordered,
    po.quantity,
    po.unit,
    po.buyer,
    pf.invoice_filename as invoice,
    pf.invoice_faktura_filename as invoice_faktura
    FROM public.orders po
    LEFT OUTER JOIN public.files pf
    ON po.id = pf.order_id
    WHERE po.buyer = '{buyer}'
    ORDER BY po.id
"""


@query(connector)
def get_orders():
    return f"""SELECT
    po.id,
    po.article,
    po.product_name,
    po.product_naming,
    po.brand,
    po.quantity_ordered,
    po.quantity,
    po.unit,
    b.buyer_name AS Заказчик,
    pf.invoice_filename as invoice,
    pf.invoice_faktura_filename as invoice_faktura
    FROM public.orders po
    LEFT OUTER JOIN public.files pf
    ON po.id = pf.order_id
    LEFT OUTER JOIN public.buyer b 
    ON po.buyer = b.buyer_id
    ORDER BY po.id
"""