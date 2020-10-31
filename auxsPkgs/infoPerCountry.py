
import os
import sys
import pathlib
import pandas as pd

import auxsPkgs.infoPerCountryAuxClasses

import datetime
import auxsPkgs.auxsDateTimeMoment

basePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def printTitle(text, nChars): 
	if len(text)>nChars: 
		print(text[0:nChars])
		showCentered(text[(nChars+1):], nChars)
	else: 
		sideSymbols = int((nChars - len(text))*0.5-1) * "="
		print("="*nChars)
		print(sideSymbols + " " + text + " " + sideSymbols)
		print("="*nChars)

def updateData(): 
	printTitle("Updating Data from Countries", 150)
	columns = auxsPkgs.infoPerCountryAuxClasses.Columns()
	# Se crea objeto con todos los paises conocidos
	countries = auxsPkgs.infoPerCountryAuxClasses.Countries()
	# Se encuentra ultima fecha de actualizacion en cualquier pais
	maxMoment = auxsPkgs.auxsDateTimeMoment.Moment(auxsPkgs.auxsDateTimeMoment.Date(1,1,2000), auxsPkgs.auxsDateTimeMoment.Time(0,0,0))
	for country in countries.countries: 
		for i in range(len(country.date)): 
			date = country.date[i].split("/")
			time = country.time[i].split(":")
			moment = auxsPkgs.auxsDateTimeMoment.Moment(auxsPkgs.auxsDateTimeMoment.Date(int(date[0]),int(date[1]),int(date[2])), auxsPkgs.auxsDateTimeMoment.Time(int(time[0]),int(time[1]),int(time[2])))
			if moment>maxMoment: maxMoment = moment
	maxDate = maxMoment.date
	maxTime = maxMoment.time
	print("\tLatest data updated: " + str(maxMoment))
	# Se utilizan datos posteriores a ultima fecha de actualizacion encontrada para seguir actualizando paises desde ahi en adelante
	path = basePath + "/Data/updates"
	folders = [x[0] for x in os.walk(path)]
	# Se enlistan las carpetas que hay, cada uno correspondiente a una fecha
	datesIDs = [folders[i+1].split("/")[-1] for i in range(len(folders)-1)]
	dates = [auxsPkgs.auxsDateTimeMoment.Date(int(date.split("_")[2]), int(date.split("_")[1]), int(date.split("_")[0])) for date in datesIDs]
	dates = [date for date in dates if date>=maxDate]
	datesIDs = [str(date).split("/")[2]+"_"+str(date).split("/")[1]+"_"+str(date).split("/")[0] for date in dates]
	for i in range(len(datesIDs)): 
		dateID = datesIDs[i]
		date = auxsPkgs.auxsDateTimeMoment.Date(int(dateID.split("_")[2]), int(dateID.split("_")[1]), int(dateID.split("_")[0]))
		print("\t\t - Updating tables from " + str(date))
		dateFolder = path + "/" + dateID
		filesPath = [(dateFolder + "/" + f) for f in os.listdir(dateFolder) if os.path.isfile(os.path.join(dateFolder, f))]
		for filePath in filesPath:
			momentString = filePath.split("/")[-1].split(".")[0]
			time = auxsPkgs.auxsDateTimeMoment.Time(int(momentString.split(" ")[1].split("_")[0]), int(momentString.split(" ")[1].split("_")[1]), int(momentString.split(" ")[1].split("_")[2]))
			moment = auxsPkgs.auxsDateTimeMoment.Moment(date, time)
			if moment>maxMoment:
				table = pd.read_csv(filePath)	
				names = columns.getNames(table)
				countries.update(table, moment, names)
	countries.saveData(path)
	print("\tData has been updated. Process finished. ")






















