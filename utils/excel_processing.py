from openpyxl.reader.excel import load_workbook
import operator

from app import app

operations = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}


def find_cell_by_value(filename, search_value, number_column):  # noqa C901
    """
    Находит ячейку по значению в файле Excel.

    Args:
        filename:  Имя файла Excel.
        search_value: Значение для поиска.

    Returns:
        Кортеж (row, column) с координатами ячейки, если найдена,
        иначе None.
    """
    try:
        workbook = load_workbook(filename)
        for cell in [x for x in workbook.active.columns][number_column]:
            if cell.value == search_value:
                return cell.row, cell.column

        app.server.logger.info(f"Значение '{search_value}' не найдено в файле '{filename}'.")

    except FileNotFoundError:
        app.server.logger.info(f"Ошибка: Файл '{filename}' не найден.")
        return None
    return None


def update_cell_by_value(filename, row, column, math_operation, value):

    try:
        workbook = load_workbook(filename, data_only=True)
        current_value = workbook.active.cell(row=row, column=column).value
        workbook.active.cell(row=row, column=column).value = operations[math_operation](current_value, value)
        workbook.save(filename)
    except TypeError:
        return False
    except FileNotFoundError:
        return False

    return True


def get_value_by_location(filename, row, column):

    try:
        workbook = load_workbook(filename, data_only=True)
    except FileNotFoundError:
        app.server.logger.info(f"Ошибка: Файл '{filename}' не найден.")
        return None

    return workbook.active.cell(row=row, column=column).value
