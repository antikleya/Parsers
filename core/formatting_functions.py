def space_delete(inp):
    """
    Removes a space in the beginning of the input string if it exists

    :param inp: Input string
    :return: Corrected string
    :rtype: str
    """

    if inp[0] == ' ':
        return inp[1:]
    return inp


def get_str_table_struct(table_struct):
    """
    Makes a string from a table structure that can be passed into an sql query

    :param table_struct: A list of fields in a format of (name, type, modifiers).
    If modifiers are passed they must start with a space
    :return: string table structure
    :rtype: str
    """

    str_table_struct = ''
    length = len(table_struct)
    for i in range(length - 1):
        str_table_struct += table_struct[i][0] + ' '*(30 - len(table_struct[i][0]) - len(table_struct[i][1])) \
                            + table_struct[i][1] + table_struct[i][2] + ',\n'
    i = length - 1
    str_table_struct += table_struct[i][0] + ' '*(30 - len(table_struct[i][0]) - len(table_struct[i][1])) \
                        + table_struct[i][1] + table_struct[i][2]
    return str_table_struct
