from datetime import datetime
import sqlite3
from core import return_codes, get_str_table_struct
from settings import wildberries_table_structure


def db_save(row, table_name, column_number):
    """
    Saves given row into the given table inside sqlite3 database

    :param row: Row must be a tuple in the same format as the table
    :param table_name: Must be a name of an existing table in the database
    :param column_number: Number of columns
    :return: returns one of the return codes from core
    """
    try:
        connection = sqlite3.connect('../ParsingResults.db')
        cursor = connection.cursor()
        cursor.execute(f"INSERT or REPLACE INTO {table_name} VALUES ({'?,' * (column_number - 1) + '?'})", row)
        connection.commit()
        connection.close()
        return return_codes['OK']
    except Exception:
        return return_codes['Error']


save_options = {'.db': db_save}


def create_table(table_structure):
    date = datetime.today().strftime('%d_%m_%Y_%H_%M')
    table_name = f'WildBerries_{date}'
    connection = sqlite3.connect('../ParsingResults.db')
    cursor = connection.cursor()
    str_table_structure = get_str_table_struct(table_structure)
    cursor.execute(f"""CREATE TABLE {table_name} ({str_table_structure});""")
    connection.commit()
    connection.close()
    return table_name


def save_row(row, table_name, save_option, table_structure):
    if save_option == save_options['.db']:
        save_option(row, table_name, len(table_structure))
