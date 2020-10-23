
import pathlib
import os
import pandas as pd
import numpy as np
import csv

class Country: 
	def __init__ (self, formalName):
		self.formalName = formalName
		self.myPath = self.getMyPath()
		self.names = self.getNames()
		self.getData()
		# self.population = self.getPopulation()
	def getData(self): 
		filePath = self.myPath + "/" + self.formalName + ".csv"
		if not os.path.exists(filePath): 
			self.totalCases = []
			self.totalDeaths = []
			self.totalRecoveries = []
			self.totalTests = []
			self.population = []
			self.date = []
			self.time = []
			return
		table = pd.read_csv(filePath)
		self.totalCases = table["totalCases"].values.tolist()
		self.totalDeaths = table["totalDeaths"].values.tolist()
		self.totalRecoveries = table["totalRecoveries"].values.tolist()
		self.totalTests = table["totalTests"].values.tolist()
		self.population = table["Population"].values.tolist()
		self.date = table["date"].values.tolist()
		self.time = table["time"].values.tolist()
	def getNames(self): 
		filePath = self.myPath + "/myNames.txt"
		if not os.path.exists(filePath): 
			fileObject = open(filePath, "w+")
			fileObject.write(self.formalName + "\n")
			fileObject.close()
			return set({self.formalName})
		else: 
			newSet = set()
			fileObject = open(filePath, "r")
			for name in fileObject.readlines(): 
				newSet.add(name.rstrip())
			fileObject.close()
			return newSet
		set({formalName})
	def addName(self, name): 
		filePath = self.myPath + "/myNames.txt"
		fileObject = open(filePath, "a+")
		fileObject.write(name + "\n")
		fileObject.close()
		self.names.add(name)
	def getMyPath(self): 
		path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/Data/countries/" + self.formalName
		if not os.path.exists(path): 
			os.mkdir(path)
		return path
	def getDF(self):
		return pd.DataFrame({
			"totalCases": self.totalCases, 
			"totalRecoveries": self.totalRecoveries, 
			"totalDeaths": self.totalDeaths, 
			"totalTests": self.totalTests, 
			"Population": self.population, 
			"date": self.date, 
			"time": self.time
			})
	def showData(self): print(self.getDF())
	# actualizar los datos del pais con lo que aparezca en cierta fila (que se sabe que habla de ese pais), 
	# que contiene lo referente al instante moment
	# el diccionario names dice, para cada atributo, como se llama la columna que lo contiene
	def update(self, row, moment, names):
		cases = row.loc[names["cases"]]
		if type(cases)==str: 
			cases = cases.replace(",","").replace(".","").replace(" ","")
			if cases=="": 
				cases = 0
			else: 
				cases = int(cases)
		if np.isnan(cases): cases = None
		deaths = row.loc[names["deaths"]]
		if type(deaths)==str: 
			deaths = deaths.replace(",","").replace(".","").replace(" ","")
			if deaths=="": 
				deaths = 0
			else: 
				deaths = int(deaths)
		if np.isnan(deaths): deaths = None
		if names["recoveries"]!=None: 
			recoveries = row.loc[names["recoveries"]]
			if type(recoveries)==str: 
				recoveries = recoveries.replace(",","").replace(".","").replace(" ","")
				if recoveries=="": 
					recoveries = 0
				else: 
					recoveries = int(recoveries)
			if np.isnan(recoveries): recoveries = None
		else: 
			recoveries = None
		if names["tests"]!=None: 
			tests = row.loc[names["tests"]]
			if type(tests)==str: 
				tests = tests.replace(",","").replace(".","").replace(" ","")
				if tests=="": 
					tests = 0
				else: 
					tests = int(tests)
			if np.isnan(tests): tests = None
		else: 
			tests = None
		if names["population"]!=None: 
			population = row.loc[names["population"]]
			if type(population)==str: 
				population = population.replace(",","").replace(".","").replace(" ","")
				if population=="": 
					population = 0
				else: 
					population = int(population)
			if np.isnan(population): population = None
		else: 
			population = None
		if (len(self.totalCases)==0): 
			self.totalCases.append(cases)
			self.totalDeaths.append(deaths)
			self.totalRecoveries.append(recoveries)
			self.totalTests.append(tests)
			self.population.append(population)
			self.date.append(str(moment.date))
			self.time.append(str(moment.time))
		elif (cases != self.totalCases[-1]) | (deaths != self.totalDeaths[-1]) | (recoveries != self.totalRecoveries[-1]) | (tests != self.totalTests[-1]): 
			self.totalCases.append(cases)
			self.totalDeaths.append(deaths)
			self.totalRecoveries.append(recoveries)
			self.totalTests.append(tests)
			self.population.append(population)
			self.date.append(str(moment.date))
			self.time.append(str(moment.time))
	# Guarda la tabla correspondiente al pais, en CSV, en el path indicado 
	def saveData(self): 
		self.getDF().to_csv(str(self.myPath) + "/" + self.formalName + ".csv")

class Countries:
	def __init__(self):
		self.myPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/Data/countries"
		self.countries = self.readCountries()
		self.notCountries = self.readNotCountries()
		self.saved = False
	def readCountries(self): 
		path = self.myPath
		countries = [x[0].split("/")[-1] for x in os.walk(path)]
		countries.remove("countries")
		newArr = []
		for country in countries: 
			newArr.append(Country(country))
		return newArr
	def readNotCountries(self): 
		filePath = self.myPath + "/NotCountries.txt"
		if not os.path.exists(filePath): 
			return set()
		else: 
			newSet = set()
			fileObject = open(filePath, "r")
			for notCountry in fileObject.readlines(): 
				newSet.add(notCountry.rstrip())
			fileObject.close()
			return newSet
	def addNotCountry(self, notCountry): 
		filePath = self.myPath + "/NotCountries.txt"
		if not os.path.exists(filePath): 
			fileObject = open(filePath, "w+")
		else: 
			fileObject = open(filePath, "a+")
		fileObject.write(notCountry + "\n")
		fileObject.close()
		self.notCountries.add(notCountry)
	def update(self, table, moment, names): 
		for i in range(len(table)): 
			row = table.iloc[i]
			name = row[names["countries"]].replace("\n","").strip()
			if (name in self.notCountries): continue
			country = self.getCountry(name)
			if country == None: continue
			country.update(row, moment, names)
	# Dado el nombre de un pais, se busca a cual corresponde
	# Si no existe en la base, se crea el nombre (y de ser necesario, el pais)
	def getCountry(self, nameCountry): 
		# para cada pais que ya existe, se ve si el nombre ingresado es uno de los correspondientes
		if nameCountry in self.notCountries: 
			return None
		for i in range(len(self.countries)): 
			country = self.countries[i]
			if nameCountry in country.names: 
				return country
		# Si nombre no es de nadie, se agrega al pais correspondiente (de ser necesario, se crea el pais)
		self.addCountryName(nameCountry)
		return self.getCountry(nameCountry)
	# Dado el nombre de un pais, si corresponde, se agrega a un pais existente, si no, se crea el pais necesario
	def addCountryName(self, nameCountry): 
		# Si lista esta vacia, se crea directamente
		if len(self.countries)==0: 
			self.countries.append(Country(nameCountry))
		else: 
			# Se verifica a que pais corresponderia el nombre indicado
			print("QUESTION: ")
			print("\tIs ==" + nameCountry + "== a reference to any of the following countries (if so, enter the number). \n\tIf is a new country, enter 0. \n\tIf it is not a country, enter -1. ") 
			for i in range(len(self.countries)): 
				text = "\t\t" + str(i+1) + ".- " + self.countries[i].formalName
				if len(self.countries[i].names)>1: 
					text += " ("
					for name in self.countries[i].names: 
						text+= (name+", ")
					text = text[:-2] + ")"
				print(text)
			ans = input("\tYour answer for " + nameCountry + ": ") 
			try: 
				ansNumber = int(ans)
			except: 
				print("Invalid input. ") 
				self.addCountryName(nameCountry)
			else:
				if (ansNumber<-1 | ansNumber>len(self.countries)): 
					print("Invalid input. ") 
					self.addCountryName(nameCountry)
				# si se ingreso 0, se crea el pais nuevo
				elif ansNumber == 0: 
					self.countries.append(Country(nameCountry))
				# si se ingreso -1, la entidad en cuestion no es un pais (o no es un pais que queremos guardar)
				elif ansNumber == -1: 
					self.addNotCountry(nameCountry)
				# si input fue valido y no 0, se agrega nombre a pais correspondiente
				else: 
					self.countries[ansNumber-1].addName(nameCountry)
	# Dado un basePath, escribe los datos correspondientes a cada pais en un csv
	def saveData(self, path): 
		for i in range(len(self.countries)): 
			self.countries[i].saveData()
		self.saved = True
			

# Objeto que guarda todos los nombres utilizados para las columnas que interesan
class Columns: 
	# Inicializamos los arreglos de nombres con los que mas se espera que aparezcan
	def __init__ (self): 
		self.myPath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/Data/columns"
		self.casesNames = self.readNames("cases")
		self.deathsNames = self.readNames("deaths")
		self.recoveriesNames = self.readNames("recoveries")
		self.testsNames = self.readNames("tests")
		self.populationNames = self.readNames("population")
		self.junkNames = self.readNames("junk")
	def readNames(self, colName): 
		filePath = self.myPath + "/"+colName+".txt"
		if not os.path.exists(filePath): 
			return []
		else: 
			newArr = []
			fileObject = open(filePath, "r")
			for notCountry in fileObject.readlines(): 
				newArr.append(notCountry.rstrip())
			fileObject.close()
			return newArr
	def writeName(self, newName, colName): 
		filePath = self.myPath + "/" + colName + ".txt"
		if not os.path.exists(filePath): 
			fileObject = open(filePath, "w+")
		else: 
			fileObject = open(filePath, "a+")
		fileObject.write(newName + "\n")
		fileObject.close()
	# dado un dataframe, entrega un dictionario con el nombre de la columna que contiene cada info
	# Si info no es parte de la tabla, entrega un None en esa instancia
	def getNames(self, table): 
		possibleNames = []
		for column in table.columns: 
			if not(column in self.junkNames): 
				possibleNames.append(column)
		d = dict()
		found = False
		# Para cada una de las cinco informaciones relevantes, se busca la columna que lo contiene
		# Si alguna info no tiene ningun nombre dentro de la tabla, se le pregunta la usuario cual es
		for i in range(len(possibleNames)):
			column = possibleNames[i] 
			if "China" in table[column].array: 
				d["countries"] = column
				possibleNames.pop(i)
				break
		for i in range(len(possibleNames)):
			column = possibleNames[i] 
			if column in self.casesNames: 
				d["cases"] = column
				found = True
				possibleNames.pop(i)
				break
		if (not found) and (len(possibleNames)>0): 
			d["cases"] = self.addName(possibleNames, "cases")
			if d["cases"]!=None: possibleNames.remove(d["cases"])
		elif (len(possibleNames)==0) & (not found): 
			d["cases"] = None
		found = False
		for i in range(len(possibleNames)):
			column = possibleNames[i] 
			if column in self.deathsNames: 
				d["deaths"] = column
				found = True
				possibleNames.pop(i)
				break
		if (not found) and (len(possibleNames)>0): 
			d["deaths"] = self.addName(possibleNames, "deaths")
			if d["deaths"]!=None: possibleNames.remove(d["deaths"])
		elif (len(possibleNames)==0) & (not found): 
			d["deaths"] = None
		found = False
		for i in range(len(possibleNames)):
			column = possibleNames[i] 
			if column in self.recoveriesNames: 
				d["recoveries"] = column
				found = True
				possibleNames.pop(i)
				break
		if (not found) and (len(possibleNames)>0): 
			d["recoveries"] = self.addName(possibleNames, "recoveries")
			if d["recoveries"]!=None: possibleNames.remove(d["recoveries"])
		elif (len(possibleNames)==0) & (not found): 
			d["recoveries"] = None
		found = False
		for i in range(len(possibleNames)):
			column = possibleNames[i] 
			if column in self.testsNames: 
				d["tests"] = column
				found = True
				possibleNames.pop(i)
				break
		if (not found) and (len(possibleNames)>0): 
			d["tests"] = self.addName(possibleNames, "tests")
			if d["tests"]!=None: possibleNames.remove(d["tests"])
		elif (len(possibleNames)==0) & (not found): 
			d["tests"] = None
		found = False
		for i in range(len(possibleNames)):
			column = possibleNames[i] 
			if column in self.populationNames: 
				d["population"] = column
				found = True
				possibleNames.pop(i)
				break
		if (not found) and (len(possibleNames)>0): 
			d["population"] = self.addName(possibleNames, "population")
			if d["population"]!=None: possibleNames.remove(d["population"])
		elif (len(possibleNames)==0) & (not found): 
			d["population"] = None
		for column in possibleNames: 
			if not (column in d.values()): 
				self.writeName(column, "junk")
				self.junkNames.append(column)
		return d
	# Se pregunta al usuario cual de las entradas de colNames tiene la info de name
	# Si no es ninguna, se retorna un None
	# si es alguna, se agrega ese nombre al array correspondiente y se retorna el valor
	def addName(self, colNames, name): 
		namesToCheck = []
		for colName in colNames: 
			if colName in self.casesNames: continue
			if colName in self.deathsNames: continue
			if colName in self.recoveriesNames: continue
			if colName in self.deathsNames: continue
			if colName in self.populationNames: continue
			if colName in self.junkNames: continue
			namesToCheck.append(colName)
		if len(namesToCheck)==0: 
			return None
		print("QUESTION")
		print("\tWhich of the following columns is refering to information regarding ==" + name + "== (enter 0 if none): ") 
		for i in range(len(colNames)): 
			print("\t\t" + str(i+1) + ".- " + colNames[i])
		ans = input("\tYour answer: ")
		try: 
			ansNumber = int(ans)
		except: 
			print("\tInvalid input. ") 
			return self.addName(colNames, name) 
		else: 
			if (ansNumber<0) | (ansNumber>len(colNames)): 
				print("\tInvalid input. ") 
				return self.addName(colNames, name)
			else: 
				if ansNumber == 0: 
					return None
				else: 
					output = colNames[ansNumber-1]
					if name=="cases": 
						self.writeName(output, name)
						self.casesNames.append(output)
					elif name=="deaths": 
						self.writeName(output, name)
						self.deathsNames.append(output)
					elif name=="recoveries": 
						self.writeName(output, name)
						self.recoveriesNames.append(output)
					elif name=="tests": 
						self.writeName(output, name)
						self.testsNames.append(output)
					elif name=="population": 
						self.writeName(output, name)
						self.populationNames.append(output)
					return output







