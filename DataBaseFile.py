import sqlite3

con = sqlite3.connect("DataBase.db")

cur = con.cursor()


# Поиск по базе данных
def find(operand):
    return cur.execute(operand).fetchall()[0]


# Поиск статистики
def statistics(table):
    resoult_true = cur.execute(f'''SELECT id FROM {table} WHERE
                            werdict="True"''').fetchall()
    resoult_false = cur.execute(f'''SELECT id FROM {table} WHERE
                            werdict="False"''').fetchall()
    true = len(resoult_true)
    false = len(resoult_false)
    return [str(true), str(false)]


# Сохранение настроек при изменении
def update(types):
    cur.execute('''UPDATE QuestionSettings
                    SET type1 = ?,
                        type2 = ?,
                        type3 = ?,
                        type4 = ?''', (str(types[0]), str(types[1]), str(types[2]), str(types[3])))
    con.commit()


# Внос новой статистики
def insert(werd, table):
    if werd == 'True':
        cur.execute(f'''INSERT INTO {table}(werdict) VALUES('True')''')
    elif werd == 'False':
        cur.execute(f'''INSERT INTO {table}(werdict) VALUES('False')''')
    else:
        cur.execute(f'''INSERT INTO {table}(werdict) VALUES('None')''')
    con.commit()


# Очистка статистики
def delete_qa():
    cur.execute('''DELETE from QuestionAnswers''')
    con.commit()