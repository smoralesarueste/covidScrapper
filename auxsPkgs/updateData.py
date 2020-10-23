# python /Users/sebastianmorales/Desktop/Otros/Coronavirus\ Data/updateData.py

# from auxsPkgs.auxsDateTimeMoment import *

import os
import sys
import pathlib
import pandas as pd

basePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

import datetime
from auxsPkgs.auxsDateTimeMoment import Date, Time, Moment
from auxsPkgs.auxsInternet import URL, Web_Connection, HTMLText, HTMLTable
from auxsPkgs.historicWebPage import HistoricWebPage, showProgress

def printTitle(text, nChars): 
	if len(text)>nChars: 
		print(text[0:nChars])
		showCentered(text[(nChars+1):], nChars)
	else: 
		sideSymbols = int((nChars - len(text))*0.5-1) * "="
		print("="*nChars)
		print(sideSymbols + " " + text + " " + sideSymbols)
		print("="*nChars)

# Ve los datos que ya existen y actualiza de ahi en adelante
def updateData(): 
	printTitle("Downloading new Data", 150)
	dataPath = basePath + "/Data/updates"
	folders = [x[0] for x in os.walk(dataPath)]
	# Se ve en las carpetas que existen, la fecha mas "alta"
	datesIDs = [folders[i+1].split("/")[-1] for i in range(len(folders)-1)]
	maxDate = Date(1, 1, 2000)
	for i in range(len(datesIDs)): 
		dateID = datesIDs[i]
		sepValues = dateID.split("_")
		date = Date(int(sepValues[2]),int(sepValues[1]), int(sepValues[0]))
		if i==0: 
			maxDate = date
		else:
			if date>maxDate: 
				maxDate = date
	path = dataPath+"/"+maxDate.pathString()
	files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
	maxTime = Time(0,0,0)
	# En los archivos que existen en esa fecha, se ve la de la hora mas "alta"
	for file in files:
		timeStr = file.split(" ")[1].split("_")
		time = Time(int(timeStr[0]), int(timeStr[1]),int(timeStr[2].split(".")[0]))
		if time>maxTime: 
			maxTime = time
	maxMoment = Moment(maxDate, maxTime)
	print("\tLatest table downloaded: " + str(maxMoment))
	today = Date(datetime.datetime.now().day, datetime.datetime.now().month, datetime.datetime.now().year)
	date = maxDate
	# Se itera sobre los updates posteriores al que ya se tiene
	while True: 
		print("\t\t - Extracting data from " + str(date))
		historical = HistoricWebPage("https://www.worldometers.info/coronavirus/", date, date)
		for i in range(len(historical.moments)):
			moment = historical.moments[i]
			if (moment <= maxMoment): 
				continue
			print("\t\t\t - " + str(moment.time))
			try: 
				snapshot = historical.getSnapshot(moment)
			except: 
				print("\t\t\t\t - Error connecting on " + str(moment) + ", going to the next one. ")
				continue
			else:
				tables = snapshot.bs.find_all("table")
				found = False
				for t in tables:
					if "China" in str(t):
						table = t
						# print(table)
						found = True
						break
				if found == False: 
					print("\t\t\t\t - No table found on " + str(moment) + ", going to the next one. ")
					continue
				else: 
					HTMLTable(table).saveData(moment,basePath)
		if date == today: 
			break
		else:
			date = date.next()
	print("\tAll possible Data has been downloaded. Process finished. ")



















