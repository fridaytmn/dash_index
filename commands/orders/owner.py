from utils.connectors.command_wraper import command
from queries.orders import connector


@command(connector)
def create_new_customer(
    buyer_name: str, buyer_inn: str, email=None, phone_number=None
) -> str:
    """Создание нового покупателя с ИНН, почтой и номером телефона"""
    return f"""INSERT INTO public.buyer (buyer_name, buyer_inn, email, phone_number)
    VALUES ('{buyer_name}', '{buyer_inn}', '{email}', '{phone_number}')
"""


@command(connector)
def insert_new_order(order_id: int) -> str:
    """Перенос новой заявки в таблицу Owner"""
    return f"""INSERT INTO public.owner_orders (order_id) VALUES ({order_id})"""


@command(connector)
def create_new_seller(
    seller_name: str, seller_inn: str, email=None, phone_number=None
) -> str:
    """Создание нового поставщика с ИНН, почтой и номером телефона"""
    return f"""INSERT INTO public.sellers (seller_name, seller_inn, email, phone_number)
    VALUES ('{seller_name}', '{seller_inn}', '{email}', '{phone_number}')
"""


@command(connector)
def update_seller(
    seller_id: int,
    seller_name: str,
    seller_inn: str,
    email=None,
    phone_number=None,
) -> str:
    """Обновление данных поставщика по идентификатору"""
    return f"""UPDATE public.sellers
    SET seller_name = '{seller_name}',
        seller_inn = '{seller_inn}',
        email = '{email}',
        phone_number = '{phone_number}'
    WHERE seller_id = {seller_id}"""


@command(connector)
def delete_seller(seller_id: int) -> str:
    """Удаление поставщика по идентификатору"""
    return f"DELETE FROM public.sellers WHERE seller_id = {seller_id}"
