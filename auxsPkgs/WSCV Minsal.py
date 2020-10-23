# python /Users/sebastianmorales/Desktop/Otros/Coronavirus\ Data/WSCVTS 

import os
import urllib
from bs4 import BeautifulSoup
import pandas as pd
import sys
import numpy as np
import pathlib

# Limpia la consola
def clear(): os.system('cls' if os.name == 'nt' else 'clear')

# Objetos que guardan dia - mes - ano
# Pueden transformarse a string en formato dd/mm/yyyy
# Con next() se obtiene siguiente dia (respeta anos bisiestos)
# Puede utilizar desigualdades
class Date: 
	def __init__(self, day, month, year): 
		self.day = day
		self.month = month
		self.year = year
	def isLeap(self): 
		if self.year%4>0: 
			return False
		elif self.year%100>0: 
			return True
		return self.year%400==0
	def totalMonth(self): 
		if self.month==2: 
			if self.isLeap(): 
				return 29
			else: 
				return 28
		elif self.month in [1, 3, 5, 7, 8, 10, 12]: return 31
		else: return 30
	def next(self): 
		if self.day<self.totalMonth(): 
			day = self.day + 1
			month = self.month
			year = self.year
		elif self.month <12: 
			day = 1
			month = self.month + 1
			year = self.year
		else: 
			day = 1
			month = 1
			year = self.year + 1
		return Date(day, month, year)
	def __str__(self): 
		if(self.day<10): 
			day = "0"+str(self.day)
		else: 
			day = str(self.day)
		if(self.month<10): 
			month = "0"+str(self.month)
		else: 
			month = str(self.month)
		return day + "/" + month + "/" + str(self.year)
	def pathString (self): 
		if(self.day<10): 
			day = "0"+str(self.day)
		else: 
			day = str(self.day)
		if(self.month<10): 
			month = "0"+str(self.month)
		else: 
			month = str(self.month)
		return str(self.year) + "_" + month + "_" + day
	def __gt__ (self, date2): 
		if self.year > date2.year: 
			return True
		elif self.year == date2.year: 
			if self.month > date2.month: 
				return True
			elif self.month == date2.month: 
				return self.day > date2.day
		return False
	def __lt__ (self, date2): 
		return date2 > self
	def __eq__(self,date2): 
		return ((self.year==date2.year) & (self.month==date2.month) & (self.day==date2.day))


# Objetos que guardan hora - minuto
# Pueden transformarse a string en formato hh:mm
# self.dayProgress devuelve numero en (0,1) segun cuanto tiempo del dia ha avanzado
# Puede utilizar desigualdades
class Time: 
	def __init__(self, hour, minute, second): 
		self.hour = hour
		self.minute = minute
		self.second = second
		self.dayProgress = (self.hour/24.0) + (self.minute/60.0*24.0) + (self.second/60.0*60.0*24.0)
	def __str__(self): 
		if self.second<10: 
			second = "0"+str(self.second)
		else: 
			second = str(self.second)
		if self.minute<10: 
			minute = "0"+str(self.minute)
		else: 
			minute = str(self.minute)
		if self.hour<10: 
			hour = "0"+str(self.hour)
		else: 
			hour = str(self.hour)
		return hour + ":" + minute + ":" + second
	def pathString (self): 
		return str(self).replace(":","_")
	def __gt__(self, time2): 
		return self.dayProgress > time2.dayProgress
	def __lt__(self, time2): 
		return time2 > self
	def __eq__(self, time2): 
		return self.dayProgress == time2.dayProgress

# Objeto que guarda fecha - hora
# Puede utilizar desigualdades
#  Pueden transformarse a string en formato mm:hh dd/mm/yyyy
class Moment: 
	def __init__(self, date, time): 
		self.date = date
		self.time = time
	def __gt__ (self, moment2): 
		if self.date > moment2: 
			return True
		elif self.date == moment2.date: 
			return self.time > moment2.time
		return False
	def __gt__ (self, moment2): 
		if self.date > moment2: 
			return True
		elif self.date == moment2.date: 
			return self.time > moment2.time
		return False
	def __lt__ (self, moment2): 
		return moment2 > self
	def __eq__ (self, moment2): 
		return ((self.time == moment2.time) & (self.date == moment2.date))
	def __str__ (self): 
		return str(self.date) + " " + str(self.time)
	def pathString(self): 
		return self.date.pathString() + " " + self.moment.pathString()

# Objeto que guarda toda la info referente a un link
class URL: 
	def __init__(self,url): 
		self.url = url
		self.deepRoot = self.getDeepRoot()
		self.firstHalf = self.getFirstHalf()
		self.secondHalf = self.getSecondHalf()
		self.domain = self.getDomain()
		self.pageName = self.getPageName()
		self.addresses = self.secondHalf.split("/")
	def getDeepRoot(self): 
		indexDot = self.url.find(".")
		indexColon = self.url.find(":")
		if indexColon == -1: return ""
		if (indexColon < indexDot): 
			return self.url[:indexColon+3]
		return ""
	def getFirstHalf(self): 
		if (self.deepRoot == ""): 
			return self.url[:self.url.find("/")]
		else:
			urlWithoutDR = self.url[self.url.find(":")+3:]
			return urlWithoutDR[:urlWithoutDR.find("/")]
	def getSecondHalf(self): 
		if (self.deepRoot == ""): 
			return self.url[self.url.find("/")+1:]
		else:
			urlWithoutDR = self.url[self.url.find(":")+3:]
			return urlWithoutDR[urlWithoutDR.find("/")+1:]
	def getDomain(self):
		nPoints = self.firstHalf.count(".")
		if nPoints == 1: 
			return self.firstHalf[self.firstHalf.find(".")+1:]
		else: 
			text = self.firstHalf[self.firstHalf.find(".")+1:]
			return text[text.find(".")+1:]
	def getPageName(self):
		nPoints = self.firstHalf.count(".")
		if nPoints == 1: 
			return self.firstHalf[:self.firstHalf.find(".")]
		else: 
			text = self.firstHalf[self.firstHalf.find(".")+1:]
			return text[:text.find(".")]

# Objeto que guarda conexiones a un link de internet
class Web_Connection: 
	def __init__(self,url): 
		print("============================")
		print("\tEstablishing connection... ")
		self.url = URL(url)
		self.connection = self.connect()
		self.bs = self.get_bs()
		self.html = HTMLText(str(self.bs))
		print("\tConnection created! ")
		print("============================")
	def connect(self): 
		try: 
			connection = urllib.request.urlopen(self.url.url)
		except error: 
			import time
			print("\tError connecting to " + self.url.url)
			print("\tWaitting 2 seconds to try again... ") 
			time.sleep(2)
			connection = self.connect()
		return connection
	def get_bs(self): 
		bs = BeautifulSoup(self.connection, "lxml")
		return bs
	def print_html(self): 
		print(self.bs.prettify())

# Objeto que guarda codigos html de una pag web 
class HTMLText: 
	def __init__(self, text): 
		self.text = text.split()[0]
	def cleanBody(self): 
		initIndex = self.text.find(">")+1
		finalIndex = len(self.text) - self.text[len(self.text)::-1].find("<") - 1
		return self.text[initIndex:finalIndex]
	def clean(self): 
		text = self.text
		while True: 
			if text[0] != "<": break
			else:
				text = HTMLText(text).cleanBody()
		return text

class HTMLTable: 
	def __init__(self, htmlcode, moment): 
		self.htmlCode = htmlcode
		self.data = pd.read_html(str(self.htmlCode))[0]
		self.saved = self.saveData(moment)
	def saveData(self,moment): 
		filePath = "/Users/sebastianmorales/Desktop/Otros/Coronavirus Data/Data/" + moment.date.pathString()
		path = pathlib.Path(filePath)
		if not path.exists():
			os.mkdir(path)
			path = pathlib.Path(filePath)
		self.data.to_csv(filePath + "/" + moment.date.pathString() + " " + moment.time.pathString() + ".csv")
		print("Data from " + str(moment) + " has been saved. \n")
		return True


def getUpdatesInfo(): 
	print("============================")
	print("STARTING WEBSCRAPPING... ")
	print("============================")
	print("\tData will be obtained from worldometers.info/coronavirus")
	print("============================")
	print("\tLet's get the dates of the updates, and the amount of updates made on each of them... ")
	content = Web_Connection("https://web.archive.org/__wb/calendarcaptures/2?url=https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/&date=2020&groupby=day").html.clean()
	_locals = locals()
	exec("D=dict("+content+")", _locals)
	items = _locals["D"]["items"]
	print("Items: " + str(items))
	nDates = len(items)
	nUpdates = 0
	dates = [None] * nDates
	print("\tUpdates were made in the following dates: ")
	for i in range(len(items)):
		date = items[i][0]
		nUpdates = nUpdates + items[i][2]
		if date < 1000: 
			month = int(date/100)
			day = int(date - 100 * month)
		else:
			month = int(date/100)
			day = int(date - 100 * month)
		dates[i] = Date(day, month, 2020)
		if items[i][2] == 1: 
			print("\t\t" + str(i+1) + ".- " + str(dates[i]) + ": " + str(items[i][2]) + " update was made. ")
		else: 
			print("\t\t" + str(i+1) + ".- " + str(dates[i]) + ": " + str(items[i][2]) + " updates were made. ")
	moments = [None] * nUpdates
	D = dict()
	_locals = locals()
	k = n = 0
	print("============================")
	for i in range(len(dates)): 
		date = dates[i]
		print("Getting times of updates made in " + str(date))
		content = Web_Connection("https://web.archive.org/__wb/calendarcaptures/2?url=https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19/%2F&date=" + "".join(str(date).split("/")[::-1])).html.clean()
		exec("D=dict("+content+")")
		updates = _locals["D"]["items"]
		nMoments = len(updates)
		print("\tThe following updates were made: ")
		for j in range(nMoments):
			time = str(updates[j][0])
			if len(time) < 3: 
				hour = 0
				minute = 0
				second = time
			elif len(time) == 3: 
				hour = 0
				minute = time[0]
				second = time[1:]
			elif len(time) == 4: 
				hour = 0
				minute = time[:2]
				second = time[2:]
			elif len(time) == 5: 
				hour = time[0]
				minute = time[1:3]
				second = time[3:]
			else: 
				hour = time[:2]
				minute = time[2:4]
				second = time[4:]
			hour = int(hour)
			minute = int(minute)
			second = int(second)
			moments[k] = Moment(date, Time(hour, minute, second))
			print("\t\t" + str(n+1) + ".- Update made at " + str(moments[k].time))
			k += 1
			n += 1
		n = 0
		print("============================")
	moments = moments[:k]
	print("============================")
	print("============================")
	print("\tLet's get the real data... ")
	print("============================")
	tables = [None] * len(moments)
	for i in range(len(moments)): 
		moment = moments[i]
		print("Getting data upload on " + str(moment))
		bs = Web_Connection("https://web.archive.org/web/" + "".join(str(moment.date).split("/")[::-1]) + str(moment.time).replace(":","") + "/https://www.minsal.cl/nuevo-coronavirus-2019-ncov/casos-confirmados-en-chile-covid-19").bs
		foundTables = bs.find_all("table")
		print("# tables found: " + str(len(foundTables)))
		for t in foundTables: 
			if "Arica" in str(t): 
				table = HTMLTable(t, moment)
				break
		# tables = HTMLTable(bs.find(id = "table3"), moment)
		print("Data extracted: ")
		print(table.data)
		tables[i] = table
		print("\n============================")
	print("PROCESS HAS FINISHED. ")
	print("The data has been saved in the folder Data. ") 
	print("============================")
	return(tables)



getUpdatesInfo()

# def getContentRow (row, label_nav): 
# 	text = row.strip()
# 	in_bar = False
# 	in_content = False
# 	content = ""
# 	bar = ""
# 	for char in text: 
# 		if not in_bar: 
# 			if char == "<": 
# 				in_bar = True
# 				bar = ""
# 				bar += char
# 			elif in_content: 
# 				content += char
# 		else:
# 			if in_content:
# 				bar += char
# 				if bar == "<br/>": 
# 					content += " "
# 			if char == ">":
# 					bar = ""
# 					in_bar = False
# 					in_content = True
# 	return content


# linkUpdateMoments = "https://web.archive.org/__wb/calendarcaptures/2?url=https%3A%2F%2Fwww.worldometers.info%2Fcoronavirus%2F&date=2020&groupby=day"
# dataArchives = Web_Connection(linkFechasActualizaciones)
# dataArchives = Web_Connection("https://web.archive.org/web/20200111214000/en.wikipedia.org/wiki/Coronavirus")
# dataArchives = Web_Connection("https://web.archive.org/web/20200901000000*/https://www.worldometers.info/coronavirus/")
# print(dataArchives.html.clean())
# print(dataArchives.html.text)
# calendar = dataArchives.bs.find("calendar")
# print(calendar)

# dataArchives.print_html()


# Web_Connection("https://www.google.com").print_html()





















