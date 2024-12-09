from utils.connectors.command_wraper import command
from queries.orders import connector


@command(connector)
def create_new_buyer(buyer_name: str, buyer_inn: str, email=None, phone_number=None) -> str:
    """Создание нового покупателя с ИНН, почтой и номером телефона"""
    return f"""INSERT INTO public.buyer (buyer_name, buyer_inn, email, phone_number)
    VALUES ('{buyer_name}', '{buyer_inn}', '{email}', '{phone_number}')
"""