from random import randint
def create_question():
    flag = randint(1, 25)
    if flag == 1:
        a = randint(1, 1000)
        b = 0
        return ['Напишите программу, принимающую на вход строку и выводящую её на экран. ', [a], [a, b]]
    else:
        a = randint(1, 1000)
        b = randint(1, 1000)
        if a % b == 0:
            res = [b]
        else:
            res = []
        return ['Вводится число. \nНапишите программу, выводящее это число на экран, если оно делится на ' + str(b), res, [a, b]]
