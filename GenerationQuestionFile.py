from random import randint, choice


def generation_function(types):
    ques_type = generate_type(types)
    if ques_type == 1:
        return generation_type_1()
    elif ques_type == 2:
        return generation_type_2()
    elif ques_type == 3:
        return generation_type_3()
    else:
        return generation_type_4()


def translate_to_ten(number, sistem):
    res = 0
    k = 0
    for elem in str(number)[::-1]:
        res += int(elem) * sistem ** k
        k += 1
    return res


def translate_from_ten(number, sistem):
    res = ''
    while number > 0:
        res += generation_utilies[number % sistem]
        number //= sistem
    return res[::-1]


def generate_type(types):
    return choice(types)


def generation_type_1():
    elems = []
    for i in range(randint(2, 4)):
        operand = choice(['+', '-', '*', '**'])
        if operand == '**' and elems.count('**') >= 1:
            operand = choice(['+', '-', '*'])
        if operand == '**':
            elems.append(operand)
            elems.append(randint(30, 200))
        else:
            elems.append(operand)
            elems.append(randint(100, 500))
    res = ' '.join(list(map(str, elems[1:])))
    sistem = randint(2, 10)
    number = randint(0, sistem - 1)
    answer = str(translate_from_ten(eval(res), sistem)).count(str(number))
    return [f"Значение выражения {res} записали в системе счисления с основанием {sistem}. " +
            f"Сколько цифр '{number}' содержится в этой записи?", answer]


def generation_type_2():
    limit = randint(10, 50)
    delta = choice([True, False])
    sistem = randint(2, 9)
    ques = choice(type_2_words[1])
    if not delta:
        delta_ques = 'возрастания'
    else:
        delta_ques = 'убывания'

    answer = []
    for i in range(1, limit + 1):
        num = translate_from_ten(i, sistem)
        if len(str(num)) >= 2 and str(num)[-1] == str(num)[-2]:
            answer.append(i)
    answer.sort(reverse=delta)

    return [f"Укажите через запятую в порядке {delta_ques} все десятичные натуральные числа, не превосходящие " +
            f"{limit}, запись которых в {type_2_words[0][sistem - 2]} системе счисления оканчивается на {ques}.",
            ','.join(list(map(str, answer)))]


def generation_type_3():
    num = randint(100, 500)
    x = randint(2, 10)
    y = randint(2, 9)
    new_num = translate_from_ten(translate_to_ten(num, x), y)
    for sis in range(2, x):
        if translate_from_ten(translate_to_ten(num, sis), y) == new_num:
            answer = sis
            break
    else:
        answer = x
    return [f"Чему равно наименьшее основание позиционной системы счисления x, при котором {num}x = {new_num}y?" +
            f"Ответ записать в виде целого числа.",
            answer]


def generation_type_4():
    num = randint(200, 900)
    sis = randint(2, 16)
    new_num = translate_from_ten(num, sis)
    lenght = len(new_num)
    elem = new_num[-1]
    for i in range(2, sis):
        number = translate_from_ten(num, i)
        if len(number) == lenght and number[-1] == elem:
            answer = i
            break
    else:
        answer = sis
    return [f"Запись числа {num} в системе счисления с основанием N содержит {lenght} цифры и оканчивается на {elem}." +
            "Чему равно минимально возможное основание системы счисления?",
            answer]


# constants
type_2_words = (['двоичной', 'троичной', 'четверичной', 'пятиричной', 'шестиричной', 'семиричной',
                 'восьмиричной', 'девятиричной'], ['две одинаковые цифры'])
generation_utilies = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']

