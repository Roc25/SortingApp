import os
import random
import shutil
import math

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.core.window import Window

IMAGE_EXTENSION = ["png","jpg","jpeg","mpeg","gif"]

SORTPATH = "E:/GP/cloak/Сортировка/"
FVPATH = "E:/GP/cloak/fave/"

MAINOUTPATH = "E:/GP/cloak/"
OUTPATHS = ["Арты","Мемы","photoshop работы"]

OUTPATHS.sort()

DELPATH = "E:/GP/trashbin/"


def IsImage(file):
	if file.split('.')[-1] in IMAGE_EXTENSION:
		return True
	else:
		return False

def IsFolder(file):
	if os.path.isdir(file):
		return True
	else:
		return False


def imglist_create():
	#Список файлов в директории
	global imglist
	imglist = os.listdir(SORTPATH).copy()

	#Удаляем НЕ картинки
	for i in imglist:
		if not IsImage(i):
			imglist.remove(i)
	return

def main():
	imglist_create()
	print(imglist[0])

	#Размер окна
	Window.size = (1000, 700)


def add_widgets(a,widgets):
	""" Добавление сразу нескольких виджетов
	a - То куда добавляем
	widgets - СПИСОК добавляемых виджетов 
	"""
	for i in widgets:
		a.add_widget(i)
	return

def file_rename(path):
		new_name = imglist[0] + "(0)"
		icounter = 1
		while os.path.isfile(path+new_name):
			new_name = new_name.split("(")
			new_name.pop(len(new_name)-1)
			new_name = ''.join(new_name) + f"({icounter})"
			icounter += 1
		os.rename(SORTPATH+imglist[0],SORTPATH+new_name)
		shutil.move(SORTPATH+new_name,path)

class MyApp(App):
	def next_art(self):
		imglist.pop(0)
		print(imglist[0])
		self.ButtonGL.clear_widgets()
		self.ButtonGL.cols=3
		self.ButtonGL.size_hint=[.3,.2]
		self.pic.source=SORTPATH+imglist[0]
		self.main_buttons()
		self.fvbtn.background_color=[1,1,1,.5]
		return

	def move_file(self,instance):
		#Проверка на совпадение
		if os.path.isfile(SelOutPath+"/"+instance.text+"/"+imglist[0]):
			self.similar_file(SelOutPath+"/"+instance.text+"/"+imglist[0],instance.text)
		else:
			shutil.move(SORTPATH+imglist[0], SelOutPath+"/"+instance.text)
			print(SelOutPath+"/"+instance.text)
			self.next_art()

	def back(self,instance):
		self.ButtonGL.clear_widgets()
		self.ButtonGL.cols=3
		self.ButtonGL.size_hint=[.3,.2]
		self.main_buttons()

	def img_btn_press(self,instance):
		""" Очищение Layout'а и отрисовка кнопок под папок """
		global SelOutPath
		SelOutPath = MAINOUTPATH+instance.text
		self.ButtonGL.clear_widgets()
		col_count = 1
		for i in os.listdir(MAINOUTPATH+instance.text).copy():
			if IsFolder(SelOutPath+"/"+i):
				col_count += 1
				self.ButtonGL.cols=int(math.ceil(col_count/3))
				self.ButtonGL.add_widget(Button(text=i,background_color=[1,1,1,1],on_press=self.move_file))
		self.ButtonGL.add_widget(Button(text='',background_color=[1,1,1,1],on_press=self.move_file))
		self.ButtonGL.size_hint = [.8,.2]

		self.ButtonGL.add_widget(Button(text="Назад",on_press=self.back))


	def similar_file(self,path,name):
		self.ButtonGL.clear_widgets()
		self.ButtonGL.add_widget(Button(text='В мусор',on_press=self.del_press))
		self.ButtonGL.add_widget(Button(text=name,on_press=self.rename_press))
		self.ButtonGL.size_hint=[.3,.1]
		self.pic2 = Image(source=path)
		self.imageGL.add_widget(self.pic2)


	def del_press(self,instance):
		file_rename(DELPATH)
		self.next_art()
		try:
			self.imageGL.remove_widget(self.pic2)
		except BaseException:
			pass


	def rename_press(self,instance):
		print(SelOutPath+"/"+instance.text)
		file_rename(SelOutPath+"/"+instance.text)
		self.next_art()
		self.imageGL.remove_widget(self.pic2)

	def fv_press(self,instance):
		file_rename(FVPATH)
		shutil.copy(FVPATH+imglist[0],SORTPATH)
		instance.background_color=[.5,.5,.5,.5]

	def btn_skip_press(self,instance):
		self.next_art()


	def main_buttons(self):

		#Отрисовка групповых кнопок
		for i in OUTPATHS:
			self.ButtonGL.add_widget(Button(text=i,on_press=self.img_btn_press,size=(10,10)))

		#Кнопка пропуска
		self.btn_skip = Button(text='Skip',on_press=self.btn_skip_press,size=(10,10))
		self.ButtonGL.add_widget(self.btn_skip)
		return


	def build(self):
		""""
		Построение GUI
		"""

		#Главный Layout
		main_layout = AnchorLayout()


		#Основная картинка
		self.pic = Image(source=SORTPATH+imglist[0],pos=(100,200))
		#Layout для картинки
		ImageAL = AnchorLayout(anchor_x='center', anchor_y='top')
		self.imageGL = GridLayout(cols=2, size_hint=[.8,.8])
		self.imageGL.add_widget(self.pic)

		ImageAL.add_widget(self.imageGL)

		#Кнопки с доп функций
		self.delbtn = Button(text="ВГВ",background_color=[1,1,1,.5],on_press=self.del_press)
		self.fvbtn = Button(text="*",background_color=[1,1,1,.5],on_press=self.fv_press)

		#Layout'ы для кнопок с доп функциями
		self.extrabtnGL = GridLayout(cols=2,size_hint=[.15,.1])
		self.SpecialLa = AnchorLayout(anchor_x="right", anchor_y="top")
		self.SpecialLa.add_widget(self.extrabtnGL)

		add_widgets(self.extrabtnGL,[self.fvbtn,self.delbtn])

		#Layout для основнх кнопок
		ButtonAL = AnchorLayout(anchor_x='center', anchor_y='bottom')
		self.ButtonGL = GridLayout(cols=3,size_hint=[.3,.2])

		ButtonAL.add_widget(self.ButtonGL)

		self.main_buttons()

		main_layout.add_widget(ImageAL)
		main_layout.add_widget(ButtonAL)
		main_layout.add_widget(self.SpecialLa)
		return main_layout


main()
if __name__ == '__main__':
	MyApp().run()
