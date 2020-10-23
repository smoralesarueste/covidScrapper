# python /Users/sebastianmorales/Desktop/WSCV.py 

import os
import urllib
from bs4 import BeautifulSoup
import pandas as pd
import sys

def clear(): 
	os.system('cls' if os.name == 'nt' else 'clear')

class Coronavirus: 
	def __init__(self): 
		print("============================")
		self.url_path = "https://www.worldometers.info/coronavirus/"
		self.connection = self.connect()
		self.bsoup = self.create_soup()
		self.dataFrame = self.get_table_countries()
	def connect(self): 
		print("\tStablishing connection... ")
		try: 
			connection = urllib.request.urlopen(self.url_path)
		except HTTPError as e:
		    print('Error code: ', e.code)
		except URLError as e:
		    print('Reason: ', e.reason)
		else:
			print("\tConnection created! ")
			print("============================")
		return connection
	def create_soup(self): 
		print("\tCreating BSoup... ")
		bs = BeautifulSoup(self.connection, "lxml")
		print("\tBSoup created succesfully")
		print("============================")
		return bs
	def get_table_countries(self): 
		# Dado una fila de tabla en formato html, le quita todos los <> 
		def get_content_row (row, label_nav): 
			text = row.strip()
			in_bar = False
			in_content = False
			content = ""
			bar = ""
			for char in text: 
				if not in_bar: 
					if char == "<": 
						in_bar = True
						bar = ""
						bar += char
					elif in_content: 
						content += char
				else:
					if in_content:
						bar += char
						if bar == "<br/>": 
							content += " "
					if char == ">":
							bar = ""
							in_bar = False
							in_content = True
			return content
		print("\tGetting data from table into local server... ")
		table = self.bsoup.find("table")
		headers = table.find_all("th")
		names = []
		for h in headers: 
			header = str(h)
			name = get_content_row(header,"th")
			names.append(name)
		D = dict()
		for name in names: D[name] = []
		rows = table.find_all("tr")
		for i in range(len(rows)): 
			if i == 0: 
				pass
			else:
				row = rows[i]
				elements = row.find_all("td")
				j = 0
				for column in names: 
					content = get_content_row(str(elements[j]),"td")
					j += 1
					D[column].append(content)
		print("\tData extracted ")
		print("============================")
		df = pd.DataFrame(D)
		def change_data_type (df, dt_arr):
			new_df = pd.DataFrame({})
			for j in range(len(dt_arr)):
				colname = df.columns[j]
				if dt_arr[j] == "str":
					new_col = [""] * len(df.index)
					for i in range(len(new_col)): 
						value = df[colname][i].replace(" ","").replace(".","").split()
						if type(value) == list:
							value = value[0]
						new_col[i] = value
					new_df[colname] = new_col
				elif dt_arr[j] == "int": 
					new_col = [0] * len(df.index)
					for i in range(len(new_col)):
						if df[colname][i].replace(" ","")== "": 
							new_col[i] = 0
						else:
							value = df[colname][i].replace(".","").replace(",","").replace("+","").replace("-","").split()
							if type(value) == list:
								new_col[i] = int(value[0])
							else:
								new_col[i] = int(value)
					new_df[colname] = new_col
			return new_df
		return change_data_type(df, ["str", "int", "int", "int", "int", "int", "int", "int"])
	def write_table_to_csv(self):
		# from tkinter import filedialog
		# path = filedialog.askdirectory()
		# name = input("Insert the name of the file: \t")
		def number_w0(n):
			if abs(n) >= 10: 
				return str(n)
			elif n==0: 
				return "00"
			elif n > 0: 
				return "0"+str(n)
			else:
				return "-0"+str(abs(n))
		from datetime import date
		today = date.today()
		name = "coronavirus_"+number_w0(today.day)+"_"+number_w0(today.month)+"_"+number_w0(today.year)+".csv"
		self.dataFrame.to_csv('/Users/sebastianmorales/Desktop/Otros/Coronavirus Data/'+name, index = False)




cv = Coronavirus()
print(cv.dataFrame)
cv.write_table_to_csv()

'''
while(True):
	text = input("Write a script: \n")
	if((text == "exit") | (text == "quit")):
		print("Exitting... ")
		break
	else: 
		try:
			exec(text)
		except: 
			e = sys.exc_info()[0]
			print(e)




d = cv.get_table_countries()
print(d)

table = cv.bsoup.find("table")
headers = table.find_all("th")
print(headers)
names = []
for h in headers: 
	header = str(h)
	name = get_content_row(header,"th")
	names.append(name)
	print(name)
print("============================")
D = dict()
for name in names: D[name] = []
'''





