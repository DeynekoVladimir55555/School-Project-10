import runpy


def check_answer(corr_answer, prog, input):
    prog = 'resoult_list_for_answer_of_user = []\n' + prog
    k = 0
    while 'print(' in prog:
        prog = prog.replace('print(', 'resoult_list_for_answer_of_user.append(')
    while 'input()' in prog:
        prog = prog.replace('input()', str(input[k]))
        k += 1

    with open('ProgFile.py', 'w') as file:
        file.write(prog)
    try:
        res = runpy.run_module(mod_name='ProgFile')['resoult_list_for_answer_of_user']
        if res == corr_answer:
            return [True]
        return [False, '']
    except:
        return [False, 'Возникла ошибка при запуске вашей программы']
