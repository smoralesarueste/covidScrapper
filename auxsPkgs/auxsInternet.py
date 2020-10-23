
import urllib
from bs4 import BeautifulSoup
import pandas as pd
import pathlib
import os
import time

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
		self.url = URL(url)
		self.connection = self.connect()
		self.bs = self.get_bs()
		self.html = HTMLText(str(self.bs))
	def connect(self): 
		try: 
			connection = urllib.request.urlopen(self.url.url)
		except:
		    raise Exception("ERROR TRYING TO CONNECT WITH URL " (self.url.url))
		else:
			return connection
	def get_bs(self): 
		bs = BeautifulSoup(self.connection, "lxml")
		return bs
	def printHTML(self): 
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
	def __init__(self, htmlcode): 
		self.htmlCode = htmlcode
		headers = []
		for h in htmlcode.find("tr"): 
			if "th" in str(h):
				headers.append(h.text)
		data = dict()
		for h in headers: 
			data[h] = []
		for fila in htmlcode.find_all("tr")[1:]:
			i = 0
			for dato in fila.find_all("td"): 
				data[headers[i]].append(dato.text)
				i+=1
		self.data = pd.DataFrame.from_dict(data)
		self.saved = False
	def saveData(self, moment, basePath): 
		filePath = basePath + "/Data/updates/" + moment.date.pathString()
		path = pathlib.Path(filePath)
		if not path.exists():
			os.mkdir(path)
			path = pathlib.Path(filePath)
		self.data.to_csv(filePath + "/" + moment.date.pathString() + " " + moment.time.pathString() + ".csv")
		self.saved = True
