wildberries_table_structure = [('Брэнд', 'STRING', ''),
                               ('Название', 'STRING', ''),
                               ('Цена', 'STRING', ''),
                               ('Скидка', 'STRING', ''),
                               ('Итого', 'STRING', ''),
                               ('[Популярность рейтинг]', 'STRING', ''),
                               ('Рейтинг', 'STRING', ''),
                               ('Отзывы', 'STRING', ''),
                               ('Тамбнейл', 'STRING', ''),
                               ('Артикул', 'STRING', ' UNIQUE NOT NULL')]

myshop_table_structure = [('Брэнд', 'STRING', ''),
                          ('Название', 'STRING', ''),
                          ('Серия', 'STRING', ''),
                          ('Цена', 'STRING', ''),
                          ('Скидка', 'STRING', ''),
                          ('Итого', 'STRING', ''),
                          ('Популярность', 'STRING', ''),
                          ('Тамбнейл', 'STRING', ''),
                          ('Артикул', 'STRING', ' UNIQUE NOT NULL'),
                          ('ISBN', 'STRING', '')]

detmir_table_structure = []