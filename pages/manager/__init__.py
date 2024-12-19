from queries.orders.owner import get_customers

label = "Менеджер"

UNITS = {
    1: "шт.",
    2: "уп.",
    3: "л.",
}

BUYERS = get_customers()
