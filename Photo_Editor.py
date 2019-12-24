import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QInputDialog, QColorDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import os.path
from PIL import Image as I


class Error(QWidget):
    def __init__(self, message):
        super().__init__()
        # создаю окно ошибки и вывожу текст ошибки message
        self.setGeometry(800, 470, 230, 80)
        self.setWindowTitle('ERROR')
        self.txt = QLabel(self)
        self.txt.setText(message)
        self.txt.resize(250, 40)
        self.txt.move(5, 5)


class Photo_Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        # подключаю дизайн
        uic.loadUi('дизайн.ui', self)
        self.max_w=1310
        self.max_l=920
        # подключаю класс функций и заливаю основные параметры изображения
        self.tools = Editor_tools('init.jpg', self.max_w, self.max_l, self)
        # вывожу изначальную катринку
        self.lbl.setPixmap(QPixmap(self.tools.name))
        # подключаю кнопки к соответствующим функциям
        self.btn_new.clicked.connect(self.tools.new_picture)
        self.btn_copy.clicked.connect(self.tools.copy_picture)
        self.rec_r.clicked.connect(self.tools.recoloring_picture)
        self.rec_g.clicked.connect(self.tools.recoloring_picture)
        self.rec_b.clicked.connect(self.tools.recoloring_picture)
        self.btn_roted_l.clicked.connect(self.tools.roted_l)
        self.btn_roted_r.clicked.connect(self.tools.roted_r)
        self.btn_sepia.clicked.connect(self.tools.sepia)
        self.btn_black.clicked.connect(self.tools.black)
        self.btn_negativ.clicked.connect(self.tools.negative)
        self.btn_frame.clicked.connect(self.tools.frame)


class Editor_tools:
    def __init__(self, name, x, y, base):
        # прогружаю основные данные об изображении
        self.name = name  # имя
        self.x = x  # размеры
        self.y = y
        self.base = base  # создаю ссылку на основной класс
        self.copy_ind = 1  # сколько копий у этого изображения
        self.old_proc_r = 100  # процентные составляющие цветов
        self.old_proc_g = 100
        self.old_proc_b = 100
        self.im = I.open(self.name)  # загружаю изображение

    def copy_picture(self):  # функция копирования
        # спрашиваю имя копии
        i, okBtnPressed = QInputDialog.getText(self.base,
                                               "Введите название картинки",
                                               "Копия вместе с форматом")
        if okBtnPressed:
            if not (os.path.isfile(i)):
                if i == '':  # если не указано новое имя действую по умолчанию (+(copy_ind))
                    str = '({}).'.format(self.copy_ind)
                    if os.path.isfile(
                            str.join(self.name.split('.'))):
                        self.copy_ind += 1
                        str = '({}).'.format(self.copy_ind)
                    i = str.join(self.name.split('.'))
                self.im.save(i)  # создаю копию
                self.exit_picture(i)  # вывожу картинку
            else:  # вывожу при ошибке предупреждение
                self.error1 = Error('Указанный файл уже существует')
                self.error1.show()

    def new_picture(self):  # функция новой картинки
        # спрашиваю имя новой картинки
        i, okBtnPressed = QInputDialog.getText(self.base,
                                               "Введите название картинки",
                                               "Картинка вместе с форматом")
        if okBtnPressed:
            # привожу значения по умолчанию
            self.copy_ind = 1
            self.old_proc_r = 100
            self.old_proc_g = 100
            self.old_proc_b = 100
            self.base.proc_r_sp.setValue(100)
            self.base.proc_g_sp.setValue(100)
            self.base.proc_b_sp.setValue(100)
            self.exit_picture(i)  # вывожу картинкку

    def exit_picture(self, i):  # функция вывода
        if not (os.path.isfile(i)):  # проаверка на существование файла
            self.error1 = Error('Указанный файл не существует')
            self.error1.show()  # вывод предупреждения
        else:  # вывод картинки
            self.im = I.open(i)
            x, y = self.im.size
            if 900 < x or 920 < y:  # проверка на корректность размеров картинки
                self.error2 = Error(
                    'Неверный размер картинки\nмаксимальный размер 1310x920')
                self.error2.show()  # вывод предупреждения
            else:
                self.base.lbl.resize(x, y)  # изменяю поле для изображения
                self.base.lbl.move(1000 - x // 2,
                                   250 - y // 2)  # преремещаю поле, чтобы новая картинка была посередине
                # меняю параметры изображения
                self.name = i  # имя
                self.x = x  # размеры
                self.y = y
                self.base.lbl.setPixmap(QPixmap(self.name))  # вывожу картинку в поле

    def roted_l(self):  # функция поворота картинки против часовой
        if self.name != 'init.jpg':  # проверка на начальную картинку
            if 900 < self.y or 920 < self.x:  # проверка на корректность размеров
                self.error2 = Error(
                    'Невозможно перевернуть картинку\nмаксимальный размер 1310x920')
                self.error2.show()  # вывод предупреждения
            else:
                self.im.transpose(I.ROTATE_90).save(self.name)  # поворот картинки
                self.exit_picture(self.name)  # вывод картинки

    def roted_r(self):  # функция поворота картинки по часовой
        if self.name != 'init.jpg':  # проверка на начальную картинку
            if 900 < self.y or 920 < self.x:  # проверка на корректность размеров
                self.error2 = Error(
                    'Невозможно перевернуть картинку\nмаксимальный размер 1310x920')
                self.error2.show()  # вывод предупреждения
            else:
                self.im.transpose(I.ROTATE_270).save(self.name)  # поворот картинки
                self.exit_picture(self.name)  # вывод картинки

    def sepia(self):  # функция фильтра сепия
        if self.name != 'init.jpg':  # проверка на начальную картинку
            pixels = self.im.load()#загружаю пиксели
            #изменяю цвет пикселей
            for i in range(self.x):
                for j in range(self.y):
                    col = pixels[i, j]#загружаю цвет
                    o = (col[0] + col[1] + col[2]) // 3#считаю среднюю цветовую составляющую
                    pixels[i, j] = int(o + 48), int(o + 32), int(o)#меняю цвет пикселя
            self.im.save(self.name)#сохраняю картинку
            self.exit_picture(self.name)#вывожу картинку

    def negative(self):
        if self.name != 'init.jpg':  # проверка на начальную картинку
            pixels = self.im.load()#загружаю пиксели
            #изменяю цвет пикселей
            for i in range(self.x):
                for j in range(self.y):
                    col = pixels[i, j]#загружаю цвет
                    pixels[i, j] = 255 - col[0], 255 - col[1], 255 - col[2]#меняю цвет пикселя
            self.im.save(self.name)#сохраняю картинку
            self.exit_picture(self.name)#вывожу картинку

    def black(self):
        if self.name != 'init.jpg':  # проверка на начальную картинку
            pixels = self.im.load()  # загружаю пиксели
            for i in range(self.x):
                for j in range(self.y):
                    col = pixels[i, j]  # загружаю цвет
                    c = (col[0] + col[1] + col[2]) // 3  # создаю основной цвет
                    pixels[i, j] = c, c, c  # изменяю цвет пикселя
            self.im.save(self.name)  # сохраняю изображения
            self.exit_picture(self.name)  # вывожу картинку

    def frame(self):  # функция рамки
        if self.name != 'init.jpg':  # проверка на начальную картинку
            color = QColorDialog.getColor()  # получаю цвет рамки
            fr = self.base.wheight.value()  # получаю толщину рамки
            im_n = I.new("RGB", (self.x + fr * 2, self.y + fr * 2),
                         color.name())  # создаю монотонное изображение ("рамку") с учетом толщины рамки и её цвета
            pixels = self.im.load()  # загружаю пиксели
            pixels1 = im_n.load()  # загружаю пиксели "рамки"
            # загружаю в "рамку" начальное изображение
            for i in range(self.x):
                for j in range(self.y):
                    pixels1[i + fr, j + fr] = pixels[i, j]
            self.im = im_n  # меняю изображение
            self.x += fr * 2  # меняю размеры
            self.y += fr * 2
            im_n.save(self.name)  # сохраняю изображение
            self.exit_picture(self.name)  # вывожу изображение

    def recoloring_picture(self):  # функция изменения цветовой составляющей
        if self.name != 'init.jpg':  # проверка на начальную картинку
            pixels = self.im.load()  # загружаю пиксели
            # изменяю цветовую составляющую
            for i in range(self.x):
                for j in range(self.y):
                    col = pixels[i, j]  # загружаю цвет
                    # считаю изменение цвета для каждой составляющей
                    d_r = self.base.proc_r_sp.value() / self.old_proc_r
                    d_g = self.base.proc_g_sp.value() / self.old_proc_g
                    d_b = self.base.proc_b_sp.value() / self.old_proc_b
                    pixels[i, j] = int(col[0] * d_r), int(col[1] * d_g), int(
                        col[2] * d_b)  # изменяю цвет пикселя
            #меняю процент цвета
            self.old_proc_r = self.base.proc_r_sp.value()
            self.old_proc_g = self.base.proc_g_sp.value()
            self.old_proc_b = self.base.proc_b_sp.value()
            self.im.save(self.name)#сохраняю изображение
            self.exit_picture(self.name)#вывожу изображение


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Photo_Editor()
    ex.show()
    sys.exit(app.exec_())
