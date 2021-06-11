from datetime import datetime
import sqlite3
from .constants import return_codes
from .formatting_functions import get_str_table_struct


def db_save(row, table_name, column_number):
    """
    Saves given row into the given table inside sqlite3 database

    :param row: Row must be a tuple with elements in the same order as in the table
    :param table_name: Must be a name of an existing table in the database
    :param column_number: Number of columns in the table
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


# currently supported save options
save_options = {'.db': db_save}


def create_table(table_structure, shop_name):
    """
    Makes a table for the current parse from the given table structure

    :param table_structure: A list of fields in a format of (name, type, modifiers).
    If modifiers are passed they must start with a space
    :param shop_name: Name of the target shop
    :return: table name
    :rtype: str
    """

    date = datetime.today().strftime('%d_%m_%Y_%H_%M')
    table_name = f'{shop_name}_{date}'
    connection = sqlite3.connect('../ParsingResults.db')
    cursor = connection.cursor()
    str_table_structure = get_str_table_struct(table_structure)
    cursor.execute(f"""CREATE TABLE {table_name} ({str_table_structure});""")
    connection.commit()
    connection.close()
    return table_name


def save_row(row, table_name, save_option, table_structure):
    """
    Main saving function. Save a row into the correct format depending on save_option.

    :param row: Row must be a tuple with elements in the same order as in the table
    :param table_name: If saving into sql db, must be a name of an existing table in the database
    :param save_option: Must be one of the values from 'save_options' dict
    :param table_structure: A list of fields in a format of (name, type, modifiers).
    If modifiers are passed they must start with a space
    :return:
    """

    if save_option == save_options['.db']:
        save_option(row, table_name, len(table_structure))
