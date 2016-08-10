#!/usr/bin/python
"""
Эта программа предназначена для обучения работе на PyQt4(и это главная ее функция) и поиска растров.
TODO:
1. Добавить поиск растра по городу
2. Исправить алгоритм поиска по районам(Ошибочно выдает растры, возможно ошибка алгоритма)
3. Добавить окно справки
4. По типам полилиний из dxf чертежей, есть подозрение, что существует не только 2 типа
    (к чему относить 2D-Полилинию из Када)
5. Добавить переключатель по работе программы(искать по городу или растру)
6. Сделать все КРАСИВО!!!
"""
import re
import sys
import json
from PyQt4 import Qt

import dxfgrabber       # Для обработки dxf
from dxfgrabber.tags import DXFStructureError

import forlinelist      # Для заполнения выпадающего списка названиями районов
from forfind import findrastres  # Функция поиска по координатам


@Qt.pyqtSlot(int)
# работа в ручном режиме
def takevalues():
    try:
        x_coord = float(x.text())
        y_coord = float(y.text())
        name = combobox.itemText(combobox.currentIndex())
        answer.setText(str(findrastres(name, x_coord, y_coord)))
    except ValueError:
        msgBox = Qt.QMessageBox()
        msgBox.question(msgBox, "Ошибка!", "Не введены координаты!", msgBox.Ok)

# Проверяем значения X и Y на ошибки ввода
def check():
    pattern_x = r"\d\d\d\d\d\d\d.?\d?\d?"
    if re.match(pattern_x, x.text()) is None:
        x.setText("Неправильное значение")
    pattern_y = r"\d\d\d\d\d\d.?\d?\d?"
    if re.match(pattern_y, y.text()) is None:
        y.setText("Неправильное значение")
# Работа с DXF
def showDialog():
    workdir = json.loads("settings.json")
    filename = Qt.QFileDialog.getOpenFileName(mainWindow, "Open_file", workdir["workdirectory"], "*.dxf")
    try:
        dxf = dxfgrabber.readfile(filename)
    except DXFStructureError:
        msgError = Qt.QErrorMessage()
        msgError.showMessage("Неверная структура DXF файла! "+"Введите координаты в ручном режиме.")
    all_entety = [enity for enity in dxf.entities]
    all_rastr = []
    name = combobox.itemText(combobox.currentIndex())
    # Чтение координат из файла
    for i in all_entety:
        # Ищем координаты только полилиний (Такое чувство, что есть еще какой то тип)
        if i.__class__ == dxfgrabber.dxfentities.Polyline or i.__class__ == dxfgrabber.dxfentities.LWPolyline:
            for j in i.points:
                coord_x = float(round(list(j)[0], 2))
                coord_y = float(round(list(j)[1], 2))
                # Добавление номера растра полученного из findrastres(почему то не всегда точно получаем номер)
                all_rastr.append(findrastres(name, coord_x, coord_y))
        elif i.__class__ == dxfgrabber.dxfentities.Point:
            coord_x = float(round(list(i.point)[0], 2))
            coord_y = float(round(list(i.point)[1], 2))
            if coord_x != 1323201.82 and coord_y != 416377.63:
        # Добавление номера растра полученного из findrastres(почему то не всегда точно получаем номер)
                all_rastr.append(findrastres(name, coord_x, coord_y))
        else:
            answer.setText("Не допустимые линии на чертеже!")
    # исключаем одинаковые растры
    all_rastr = set(all_rastr)
    all_rastr = list(all_rastr)
    if len(all_rastr) == 1:
        answer.setText(str(all_rastr[0]))
    else:
        text = str(all_rastr[0])
        for i in range(1,len(all_rastr)):
            text = text + ", " + all_rastr[i]
        answer.setText(text)
# Блок об авторе
def showAuthor():
    msgBox = Qt.QMessageBox()
    msgBox.question(msgBox, "Об авторе.", "Спасибо куче свободного времени.", msgBox.Ok)

def settings():
    pass

if __name__ == "__main__":
    app = Qt.QApplication(sys.argv)
    mainWindow = Qt.QMainWindow()
# Точка выхода из программы в выпадающем меню
    icon_leave = Qt.QIcon('power.png')
    leave = Qt.QAction(icon_leave,"Exit",mainWindow)
    leave.setShortcut("Ctrl+Q")
    leave.setStatusTip("Exit application")
    mainWindow.connect(leave, Qt.SIGNAL("triggered()"), Qt.SLOT("close()"))
# Диалог открытия файла
    icon_open = Qt.QIcon('eye.png')
    openFile = Qt.QAction(icon_open,"Open file", mainWindow)
    openFile.setShortcut("Ctrl+O")
    openFile.setStatusTip("Open file")
    mainWindow.connect(openFile, Qt.SIGNAL("triggered()"), showDialog)
# Окно О программе
    author = Qt.QAction("About", mainWindow)
    mainWindow.connect(author, Qt.SIGNAL("triggered()"),showAuthor)
# Справка (необходимо гуглить)
    win_help = Qt.QAction("Help", mainWindow)
# Формируем выпадающее меню
    menu = mainWindow.menuBar()
    file = menu.addMenu("&File")
    settings = menu.addMenu("&Settings")
    about = menu.addMenu("&About")
    file.addAction(openFile)
    file.addSeparator()
    file.addAction(leave)
    about.addAction(win_help)
    about.addSeparator()
    about.addAction(author)
# настройка виджетов формы
    window = Qt.QWidget()
    mainWindow.setCentralWidget(window)
    mainWindow.setWindowTitle("Поиск растра")
# Позиционирование элементов grid - Основная сетка
# hbox1 - горизонтальное выравнивание, первая строка
# hbox2 - горизонтальное выравнивание, вторая строка
    grid = Qt.QGridLayout()
    window.setLayout(grid)
    hbox1 = Qt.QHBoxLayout()
    hbox1.addStretch(1)
    hbox2 = Qt.QHBoxLayout()
    hbox2.addStretch(1)
    grid.addLayout(hbox1, 0, 0)
    grid.addLayout(hbox2, 1, 0)
# выпадающий список
    combobox = Qt.QComboBox()
    combobox.addItems(forlinelist.karts)
    hbox1.addWidget(combobox)
# 2 поля для ввода координат
    x = Qt.QLineEdit("Введите координату X")
    hbox1.addWidget(x)
    y = Qt.QLineEdit("Введите координату Y")
    hbox1.addWidget(y)
# Поле для вывода номера растра
    answer = Qt.QLineEdit()
    answer.setDisabled(True)
    hbox1.addWidget(answer)
# Кнопка для активации поиска
    ok = Qt.QPushButton("Найти")
    ok.resize(10, 10)
    hbox2.addWidget(ok)
# Связки действий
    Qt.QObject.connect(x, Qt.SIGNAL("editingFinished()"), check)
    Qt.QObject.connect(y, Qt.SIGNAL("editingFinished()"), check)
    Qt.QObject.connect(ok, Qt.SIGNAL("clicked()"), takevalues)
# инициализация окна
    mainWindow.show()
# Выход из приложения
    app.exec_()