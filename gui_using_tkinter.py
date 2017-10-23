from tkinter import *
import tkinter.messagebox
from gensim.models import Word2Vec
import os

hp_model_cbow = Word2Vec.load(os.path.join("trained_HP_model","model_cbow.w2v"))
hp_model_sg = Word2Vec.load(os.path.join("trained_HP_model","model_sg.w2v"))

def getdata(query):
	cbow_res = hp_model_cbow.most_similar(query)
	sg_res = hp_model_sg.most_similar(query)
	return cbow_res, sg_res

def validatedata(query):
	if len(query)<1:
		return False
	for x in query:
		if x==' ' or x=='\n':
			return False
	if query in hp_model_cbow.wv.vocab and query in hp_model_sg.wv.vocab:
		return True
	else:
		return False

class gui:
	def __init__(self, master):
		self.label = Label(master, text='Harry Potter Vectors', font=("TimesNewRoman",40)).grid(row =0, columnspan=4)
		self.blanklabel = Label(master, text="", font=("TimesNewRoman",40)).grid(row=1)
		self.label2 = Label(master, text = "Enter a single word", font=("TimesNewRoman",20)).grid(row = 2, column=0, columnspan=2)

		self.inputbox = Text(master, height=4, width=40)
		self.inputbox.grid(row = 2, column = 2)

		self.blanklabel2 = Label(master, text="", font=("TimesNewRoman",20)).grid(row=3)

		#Button change later
		self.submitbutton = Button(master, text="Submit", command = self.submitfunc, height=4, width = 30).grid(row=4, columnspan=4)

		self.blanklabel3 = Label(master, text="", font=("TimesNewRoman",30)).grid(row=5)

		self.reslabel = Label(master, text = "", font=("TimesNewRoman",30))
		self.reslabel.grid(row=6)

		self.blanklabel4 = Label(master, text="", font=("TimesNewRoman",30)).grid(row=7)

		self.cbow_label = Label(master, text="",font=("TimesNewRoman",20))
		self.cbow_label.grid(row = 8, column = 0, columnspan = 2)
		self.sg_label = Label(master, text="",font=("TimesNewRoman",20))
		self.sg_label.grid(row = 8, column = 2, columnspan = 2)

		self.cbow_data = []
		self.sg_data = []
		for x in range(10):
			for y in range(4):
				if y<2:
					self.cbow_data.append(Label(root, text = ""))
					self.cbow_data[-1].grid(row = x+9,column = y)
				else:
					self.sg_data.append(Label(root, text = ""))
					self.sg_data[-1].grid(row = x+9,column = y)


	def submitfunc(self):
		query = self.inputbox.get("1.0",'end-1c')
		if validatedata(query)==False:
			self.reslabel['text'] = "Bad Input!!!"
			self.cbow_label['text'] = ""
			self.sg_label['text'] = ""
			for x in range(10):
				for y in range(4):
					if y<2:
						self.cbow_data[x*2+y]['text'] = ""
					else:
						self.sg_data[x*2+y-2]['text'] = ""

			return

		self.reslabel['text'] = "Results for "+query

		res_cbow = hp_model_cbow.most_similar(query)
		res_sg = hp_model_sg.most_similar(query)

		self.cbow_label['text'] = "CBOW Results"
		self.sg_label['text'] = "Skip Gram Results"

		for x in range(10):
			for y in range(4):
				if y<2:
					self.cbow_data[x*2+y]['text'] = res_cbow[x][y]
				else:
					self.sg_data[x*2+y-2]['text'] = res_sg[x][y-2]


root = Tk()
root.geometry('1280x720')
b = gui(root)
root.mainloop()						