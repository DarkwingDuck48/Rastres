import json
import os, sys
from PyQt4 import Qt


app = Qt.QApplication(sys.argv)
with open('settings.json', 'r', encoding='utf-8') as fh: #открываем файл на чтение
    data = json.load(fh) #загружаем из файла данные в словарь data
if data["lastfile"] == "":
    link = os.path.normpath(data["workdirectory"])
else:
    link = os.path.normpath(data["lastfile"])
mainWindow = Qt.QMainWindow()
filename = Qt.QFileDialog.getOpenFileName(mainWindow, "Open_file", link)
# инициализация окна
mainWindow.show()
data["lastfile"] = filename
#запись нового значения в файл
with open ('settings.json','r+', encoding='utf-8') as fh:
    fh.write(json.dumps(data, ensure_ascii=False))

# Выход из приложения
app.exec_()