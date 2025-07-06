from openpyxl.reader.excel import load_workbook


def find_cell_by_value(filename, search_value, number_column):
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
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return None

    for cell in [x for x in workbook.active.columns][number_column]:
        if cell.value == search_value:
            return cell.row, cell.column

    print(f"Значение '{search_value}' не найдено в файле '{filename}'.")
    return None


def update_cell_by_value(filename, row, column, value):

    try:
        workbook = load_workbook(filename, data_only=True)
    except FileNotFoundError:
        return None

    try:
        workbook.active.cell(row=row, column=column).value += value
        workbook.save(filename)
    except TypeError:
        return False

    return True