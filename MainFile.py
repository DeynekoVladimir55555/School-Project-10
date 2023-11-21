import sys

from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

import DataBaseFile
import GenerationQuestionFile
import GenerationProgrammingFile
import InformationWindow
import StatisticsWindows
import MoveFunction
import ProgCheckAnswer


# Класс главного окна
class MainQuestionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis\MainQuestionWindow.ui', self)
        self.setWindowTitle('Системы счисления')
        # Передвижение на центр экрана
        MoveFunction.move_to_senter(self)

        self.initUi()
        # Получение настроек
        a = DataBaseFile.find('''SELECT * FROM QuestionSettings''')
        b = []
        self.difficulty = a[0]
        if a[1] == 'True':
            b.append(1)
        if a[2] == 'True':
            b.append(2)
        self.types = b

    def initUi(self):
        self.settingsButton.clicked.connect(self.settings)
        self.exitButton.clicked.connect(self.close_window)
        self.statisticsButton.clicked.connect(self.statistics)
        self.nextButton.clicked.connect(self.create_question)
        self.answerButton.clicked.connect(self.answer)
        self.returnButton.clicked.connect(self.return_back)

        self.questionEdit.setReadOnly(True)

    def close_window(self):
        self.close()

    def settings(self):
        sw.show()

    def return_back(self):
        self.close()
        cw.show()

    def statistics(self):
        statw.show()

    def answer(self):
        # Проверка ответа
        if self.answerEdit.text() == str(self.answer):
            self.answerLabel.setText('Верно')
            # Запись правильно решённой задачи
            DataBaseFile.insert('True', 'QuestionAnswers')
        else:
            self.answerLabel.setText('Неверно')

    def create_question(self, flag=False):
        if not flag:
        # Запись неправильно решённой задачи
            if self.answerLabel.text() != 'Верно':
                DataBaseFile.insert('False', 'QuestionAnswers')
        self.nextButton.setEnabled(False)
        # Генерация задачи
        n = GenerationQuestionFile.print_question(self.difficulty, self.types)
        self.answer = n[1]
        self.questionEdit.setText(n[0])
        self.answerLabel.setText('')
        self.answerEdit.setText('')
        self.nextButton.setEnabled(True)


class MainProgrammingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis\MainProgrammingWindow.ui', self)
        self.setWindowTitle('Программирование')
        self.initUi()

    def initUi(self):
        self.checkButton.clicked.connect(self.check)
        self.exitButton.clicked.connect(self.exit)
        self.returnButton.clicked.connect(self.return_back)
        self.statButton.clicked.connect(self.stat)
        self.skipButton.clicked.connect(self.skip)
        self.delStatButton.clicked.connect(self.delete)

        self.questionEdit.setReadOnly(True)

    def check(self):
        werd = ProgCheckAnswer.check_answer(self.answer_quest, self.answerEdit.toPlainText(), self.numbers)
        apw.answer(werd)
        apw.show()

    def create_question(self, flag=False):
        q = GenerationProgrammingFile.create_question()
        self.answer_quest = q[1]
        self.numbers = q[2]
        self.questionEdit.setText(q[0])

    def return_back(self):
        self.close()
        cw.show()

    def stat(self):
        statqw.show()

    def exit(self):
        self.close()
    def skip(self):
        DataBaseFile.insert('None', 'ProgAnswers')
        self.answerEdit.setText('')
        self.create_question()

    def delete(self):
        DataBaseFile.delete_pa()


class AnswerProgrammingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis\AnswerProgrammingWindow.ui', self)
        self.setWindowTitle('Ответ')
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.flag = False
        self.initUi()

    def initUi(self):
        self.retryButton.clicked.connect(self.retry)
        self.nextButton.clicked.connect(self.next)

    def answer(self, werd):
        if werd[0] == True:
            self.retryButton.setEnabled(False)
            self.werdEdit.setText('''Вердикт:\nВерно''')
            self.flag = True
        else:
            self.werdEdit.setText(f'''Вердикт:\nНеверно\n{werd[1]}''')

    def retry(self):
        self.close()

    def next(self):
        if self.flag:
            DataBaseFile.insert('True', 'ProgAnswers')
        else:
            DataBaseFile.insert('False', 'ProgAnswers')
        self.flag = False
        self.close()
        mpw.answerEdit.setText('')
        self.retryButton.setEnabled(True)
        mpw.create_question()


# Окно выбора задач на программирование или на системы счисления
class ChoiceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis\ChoiceWindow.ui', self)
        self.setWindowTitle('Выбор задач')
        MoveFunction.move_to_senter(self)
        self.quest = False
        self.prog = False
        self.initUi()

    def initUi(self):
        self.confirmButton.clicked.connect(self.confirm)
        self.programmButton.clicked.connect(self.programming)
        self.questionButton.clicked.connect(self.question)

    def confirm(self):
        if self.prog:
            self.close()
            mpw.show()
        elif self.quest:
            self.close()
            mqw.show()

    def programming(self):
        self.prog = True
        self.quest = False

    def question(self):
        self.quest = True
        self.prog = False


# Приветственное окно
class HelloWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis\HelloWindow.ui', self)
        self.setWindowTitle('Приветствие')
        self.startWorkButton.clicked.connect(self.start)
        self.pixmap = QPixmap('files\HelloImage.jpg')
        self.image.setPixmap(self.pixmap)

        # Передвижение на центр экрана
        MoveFunction.move_to_senter(self)

    def start(self):
        self.close()
        cw.show()

# Окно настроек задач на системы счисления
class SettingsQuestionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uis\SettingsWindow.ui', self)
        self.setWindowTitle('Настройки')
        # Показывание окна поверх главного
        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        # Передвижение на центр экрана
        MoveFunction.move_to_senter(self)
        self.initUi()

    def initUi(self):
        self.cancelButton.clicked.connect(self.close_window)
        self.acceptButton.clicked.connect(self.save)
        self.informationButton.clicked.connect(self.show_information)
        self.typesBox.clicked.connect(self.choice_type)
        self.easyButton.clicked.connect(self.easy)
        self.normalButton.clicked.connect(self.normal)
        self.hardButton.clicked.connect(self.hard)
        self.clearStatisticsButton.clicked.connect(DataBaseFile.delete_qa)
        self.normalButton.setChecked(True)
        # Получение настроек при запуске
        a = DataBaseFile.find('''SELECT * FROM QuestionSettings''')

        self.type1Box.setEnabled(False)
        self.type2Box.setEnabled(False)
        self.difficulty = a[0]
        if a[1] == 'True':
            self.type1Box.setChecked(True)
        else:
            self.type1Box.setChecked(False)
        if a[2] == 'True':
            self.type2Box.setChecked(True)
        else:
            self.type2Box.setChecked(False)

    def close_window(self):
        # Закрытие и возвращение изменений
        self.errorLabel.setText('')
        a = DataBaseFile.find('''SELECT * FROM QuestionSettings''')
        self.difficulty = a[0]
        if self.difficulty == 1:
            self.easyButton.setChecked(True)
        elif self.difficulty == 2:
            self.normalButton.setChecked(True)
        elif self.difficulty == 3:
            self.hardButton.setChecked(True)
        if a[1] == 'True':
            self.type1Box.setChecked(True)
        else:
            self.type1Box.setChecked(False)
        if a[2] == 'True':
            self.type2Box.setChecked(True)
        else:
            self.type2Box.setChecked(False)
        self.close()

    def show_information(self):
        iw.show()

    def easy(self):
        self.difficulty = 1

    def normal(self):
        self.difficulty = 2

    def hard(self):
        self.difficulty = 3

    def save(self):
        # Проверка на наличие хотя бы 1 типа в генерации
        if not (self.type1Box.isChecked() or self.type2Box.isChecked()):
            self.errorLabel.setText('Вы не выбрали тип задач.')
        else:
            self.errorLabel.setText('')
            # Закрытие и сохранение изменений
            types = [self.type1Box.isChecked(), self.type2Box.isChecked()]
            DataBaseFile.update(self.difficulty, types)
            a = DataBaseFile.find('''SELECT * FROM QuestionSettings''')
            b = []
            mqw.difficulty = a[0]
            if a[1] == 'True':
                b.append(1)
            if a[2] == 'True':
                b.append(2)
            mqw.types = b
            self.close()

    def choice_type(self):
        # Вкл-выкл выбора типов задач(пользователем)
        if self.typesBox.isChecked():
            self.type1Box.setEnabled(True)
            self.type2Box.setEnabled(True)
        else:
            self.type1Box.setEnabled(False)
            self.type2Box.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mqw = MainQuestionWindow()
    mqw.create_question(flag=True)
    mpw = MainProgrammingWindow()
    mpw.create_question(flag=True)
    apw = AnswerProgrammingWindow()
    statqw = StatisticsWindows.StatisticsProgrammingWindow()
    cw = ChoiceWindow()
    sw = SettingsQuestionWindow()
    statw = StatisticsWindows.StatisticsQuestionWindow()
    iw = InformationWindow.InformationWindow()
    hw = HelloWindow()
    hw.show()
    sys.exit(app.exec_())
