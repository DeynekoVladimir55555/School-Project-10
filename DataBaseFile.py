import sqlite3

con = sqlite3.connect("DataBase.db")

cur = con.cursor()
#Поиск по базе данных
def find(operand):
    return cur.execute(operand).fetchall()[0]
#Поиск статистики
def statistics(table):
    resoult_true = cur.execute(f'''SELECT id FROM {table} WHERE
                            werdict="True"''').fetchall()
    resoult_false = cur.execute(f'''SELECT id FROM {table} WHERE
                            werdict="False"''').fetchall()
    if table == 'ProgAnswers':
        resoult_none = cur.execute(f'''SELECT id FROM ProgAnswers WHERE
                            werdict="None"''').fetchall()
    else:
        resoult_none = ''
    true = len(resoult_true)
    false = len(resoult_false)
    none = len(resoult_none)
    return [str(true), str(false), str(none)]
#Сохранение настроек при изменении
def update(difficulty, types):
    cur.execute('''UPDATE QuestionSettings
                    SET difficulty = ?,
                        type1 = ?,
                        type2 = ?''', (difficulty, str(types[0]), str(types[1])))
    con.commit()
#Внос новой статистики
def insert(werd, table):
    if werd == 'True':
        cur.execute(f'''INSERT INTO {table}(werdict) VALUES('True')''')
    elif werd == 'False':
        cur.execute(f'''INSERT INTO {table}(werdict) VALUES('False')''')
    else:
        cur.execute(f'''INSERT INTO {table}(werdict) VALUES('None')''')
    con.commit()
#Очистка статистики
def delete_qa():
    cur.execute('''DELETE from QuestionAnswers''')
    con.commit()

def delete_pa():
    cur.execute('''DELETE from ProgAnswers''')
    con.commit()