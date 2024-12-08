from utils.connectors.command_wraper import command
from queries.orders import connector


@command(connector)
def create_new_order(article: str, product_name: str, brand: str, quantity_ordered: int, quantity:str, unit: int, buyer: str) -> str:
    """Создает новую запись с начальной информацией о пользователе. версии и названии отчета и параметрами"""
    return f"""INSERT INTO public.orders (article, product_name, product_naming, brand, quantity_ordered, quantity, unit, buyer)
    VALUES ('{article}', '{product_name}', 'test_article' ,
            '{brand}', '{quantity_ordered}',
             '{quantity}', '{unit}', '{buyer}')
"""
