import sys

from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

import DataBaseFile
import GenerationQuestionFile
import InformationWindow
import StatisticsWindows
import MoveFunction


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

        self.questionEdit.setReadOnly(True)

    def close_window(self):
        self.close()

    def settings(self):
        sw.show()

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
        n = GenerationQuestionFile.generation_function(self.types)
        self.answer = n[1]
        self.questionEdit.setText(n[0])
        self.answerLabel.setText('')
        self.answerEdit.setText('')
        self.nextButton.setEnabled(True)


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
        mqw.show()


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
        self.clearStatisticsButton.clicked.connect(DataBaseFile.delete_qa)
        # Получение настроек при запуске
        a = DataBaseFile.find('''SELECT * FROM QuestionSettings''')

        self.type1Box.setEnabled(False)
        self.type2Box.setEnabled(False)
        self.type3Box.setEnabled(False)
        self.type4Box.setEnabled(False)
        if a[0] == 'True':
            self.type1Box.setChecked(True)
        else:
            self.type1Box.setChecked(False)
        if a[1] == 'True':
            self.type2Box.setChecked(True)
        else:
            self.type2Box.setChecked(False)
        if a[2] == 'True':
            self.type3Box.setChecked(True)
        else:
            self.type3Box.setChecked(False)
        if a[3] == 'True':
            self.type4Box.setChecked(True)
        else:
            self.type4Box.setChecked(False)

    def close_window(self):
        # Закрытие и возвращение изменений
        self.errorLabel.setText('')
        a = DataBaseFile.find('''SELECT * FROM QuestionSettings''')
        if a[0] == 'True':
            self.type1Box.setChecked(True)
        else:
            self.type1Box.setChecked(False)
        if a[1] == 'True':
            self.type2Box.setChecked(True)
        else:
            self.type2Box.setChecked(False)
        if a[2] == 'True':
            self.type3Box.setChecked(True)
        else:
            self.type3Box.setChecked(False)
        if a[3] == 'True':
            self.type4Box.setChecked(True)
        else:
            self.type4Box.setChecked(False)
        self.close()

    def show_information(self):
        iw.show()

    def save(self):
        # Проверка на наличие хотя бы 1 типа в генерации
        if not (self.type1Box.isChecked() or self.type2Box.isChecked() or self.type3Box.isChecked() or
        self.type4Box.isChecked()):
            self.errorLabel.setText('Вы не выбрали тип задач.')
        else:
            self.errorLabel.setText('')
            # Закрытие и сохранение изменений
            types = [self.type1Box.isChecked(), self.type2Box.isChecked()]
            DataBaseFile.update(types)
            b = []
            if types[0] == 'True':
                b.append(1)
            if types[1] == 'True':
                b.append(2)
            if types[2] == 'True':
                b.append(3)
            if types[3] == 'True':
                b.append(4)
            mqw.types = b
            self.close()

    def choice_type(self):
        # Вкл-выкл выбора типов задач(пользователем)
        if self.typesBox.isChecked():
            self.type1Box.setEnabled(True)
            self.type2Box.setEnabled(True)
            self.type3Box.setEnabled(True)
            self.type4Box.setEnabled(True)
        else:
            self.type1Box.setEnabled(False)
            self.type2Box.setEnabled(False)
            self.type3Box.setEnabled(False)
            self.type4Box.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mqw = MainQuestionWindow()
    mqw.create_question(flag=True)
    sw = SettingsQuestionWindow()
    statw = StatisticsWindows.StatisticsQuestionWindow()
    iw = InformationWindow.InformationWindow()
    hw = HelloWindow()
    hw.show()
    sys.exit(app.exec_())
