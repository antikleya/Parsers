def space_delete(inp):
    if inp[0] == ' ':
        return inp[1:]
    return inp


def get_str_table_struct(table_struct):
    str_table_struct = ''
    length = len(table_struct)
    for i in range(length - 1):
        str_table_struct += table_struct[i][0] + ' '*(30 - len(table_struct[i][0]) - len(table_struct[i][1])) \
                            + table_struct[i][1] + table_struct[i][2] + ',\n'
    i = length - 1
    str_table_struct += table_struct[i][0] + ' '*(30 - len(table_struct[i][0]) - len(table_struct[i][1])) \
                        + table_struct[i][1] + table_struct[i][2]
    return str_table_struct
