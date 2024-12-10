from queries.orders.owner import get_buyers

label = "Менеджер"

UNITS = {
    1: "шт.",
    2: "уп.",
    3: "л.",
}

BUYERS = get_buyers()
