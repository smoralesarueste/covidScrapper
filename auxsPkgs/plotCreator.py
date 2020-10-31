

import os
import sys
import pathlib
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import datetime
from math import log

import auxsPkgs.infoPerCountryAuxClasses
import auxsPkgs.auxsDateTimeMoment

from difflib import SequenceMatcher

import warnings
warnings.filterwarnings("ignore")

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

def getCountry(countries): 
	def similar(word1, word2):
		sm = SequenceMatcher(None, word1.lower(), word2.lower())
		return sm.ratio()
	countryName = input("\t- Insert the name of the country you want to plot: ")
	similarities = []
	candidates = []
	for country in countries.countries: 
		for name in country.names: 
			similarity = similar(name, countryName)
			if similarity > 0.5: 
				similarities.append(similarity)
				candidates.append(country)
				break
	if len(similarities)==0: 
		ans = input("\t\tPlease try again. Press 0 to look every known country, 1 to enter a new country name: ")
		while ans!="1" and ans!="0":
			ans = input("\t\tInvalid input. Please try again. Press 0 to look every known country, 1 to enter a new country name: ")
		if ans=="0": 
			for country in countries.countries: 
				print("\t\t\t- " + country.formalName)
		return getCountry(countries)
	elif max(similarities)>0.7: 
		candidate = candidates[similarities.index(max(similarities))]
		ans = input("\t\tDid you mean " + candidate.formalName + "? (0: no, 1: yes): ")
		while ans!="1" and ans!="0":
			ans = input("\t\tInvalid input. Did you mean " + candidate.formalName + "? (0: no, 1: yes): ")
		if ans=="1": 
			print("\t- Taking " + candidate.formalName + " as the country to be shown. ")
			return candidate
		elif len(similarities)==1: 
			print("\t\tThe country you are looking for does not match any of the knowns. ")
			ans = input("\t\tPlease try again. Press 0 to look every known country, 1 to enter a new country name. ")
			while ans!="1" and ans!="0":
				ans = input("\t\tInvalid input. Please try again. Press 0 to look every known country, 1 to enter a new country name. ")
			if ans=="0": 
				for country in countries.countries: 
					print("\t\t\t > " + country.formalName)
			return getCountry(countries)
		else: 
			print("\t\tPlease enter the number of the country you are looking for. Press -1 is the country is not there. ")
			i = 1
			for country in candidates: 
				print("\t\t\t" + str(i) + ".-\t" + country.formalName)
				i+=1
			ans = input("\n\t\t My country is number (-1 if none): ")
			while True: 
				if ans=="-1":
					return getCountry(countries)
				if not ans.isnumeric(): 
					ans = input("\n\t\t Invalid input. My country is number (-1 if none): ")
				elif int(ans)>len(candidates):
					ans = input("\n\t\t Invalid input. My country is number (-1 if none): ")
				else: 
					break
			print("\t\tTaking " + candidates[int(ans)-1].formalName + " as the country to be shown. ")
			return candidates[int(ans)-1]
	else: 
		print("\t\tNot sure the country you are looking for. ")
		if len(candidates)==1: 
			ans = input("\n\t\t Is you country " + candidates[0].formalName + "? (0: no, 1: yes): ")
			while ans!="1" and ans!="0":
				ans = input("\t\tInvalid input. Is you country " + candidates[0].formalName + "? (0: no, 1: yes): ")
			if ans=="1":
				print("\t- Taking " + candidates[0].formalName + " as the country to be shown. ")
				return candidates[0]
			else: 
				ans = input("\t\tPlease try again. Press 0 to look every known country, 1 to enter a new country name: ")
				while ans!="1" and ans!="0":
					ans = input("\t\tInvalid input. Please try again. Press 0 to look every known country, 1 to enter a new country name: ")
				if ans=="0": 
					for country in countries.countries: 
						print("\t\t\t- " + country.formalName)
				return getCountry(countries)
		else: 
			print("\t\tPlease enter the number of the country you are looking for. Press -1 is the country is not there. ")
			i = 1
			for country in candidates: 
				print("\t\t\t" + str(i) + ".-\t" + country.formalName)
				i+=1
			ans = input("\n\t\t My country is number (-1 if none): ")
			while True: 
				if ans=="-1":
					return getCountry(countries)
				if not ans.isnumeric(): 
					ans = input("\n\t\t Invalid input. My country is number (-1 if none): ")
				elif int(ans)>len(candidates):
					ans = input("\n\t\t Invalid input. My country is number (-1 if none): ")
				else: 
					break
			print("\t- Taking " + candidates[int(ans)-1].formalName + " as the country to be shown. ")
			return candidates[int(ans)-1]

def plot(country): 
	df = country.getDF()
	df["datetime"] = pd.to_datetime(df["date"] + " " + df["time"], format = "%d/%m/%Y %H:%M:%S")
	print("\t\t- Which statistics would you like to plot? ")
	print("\t\t\t1.- Total Number of Cases. ")
	print("\t\t\t2.- Total Number of Deaths. ")
	print("\t\t\t3.- Total Number of Tests. ")
	ans = input("\t\tEnter the number of the statistics you want to visualize: ")
	while True: 
		if not ans.isnumeric(): 
			ans = input("\t\tInvalid input. Enter the number of the statistics you want to visualize: ")
		elif int(ans)>3: 
			ans = input("\t\tInvalid input. Enter the number of the statistics you want to visualize: ")
		elif ans=="1": 
			y = df["totalCases"]
			title = "Total Number of Cases in " + country.formalName
			break
		elif ans=="2": 
			y = df["totalDeaths"]
			title = "Total Number of Deaths in " + country.formalName
			break
		elif ans=="3": 
			y = df["totalTests"]
			title = "Total Number of Tests in " + country.formalName
			break
	df.sort_values(by=['datetime'], inplace = True)
	plt.figure(figsize = (20,10))
	plt.grid(b = True, which = "both")
	plt.plot(df["datetime"], y)
	plt.gcf().get_axes()[0].set_title(title)
	# plt.hlines(y=0, xmin = min(df.index), xmax = max(df.index))
	plt.show()

def plotCountry(): 
	printTitle("Showing Time Series per Country", 150)
	countries = auxsPkgs.infoPerCountryAuxClasses.Countries()
	country = getCountry(countries)
	plot(country)
	ans = input("\n\tDo you want to plot another country? (y/n): ")
	# columns = auxsPkgs.infoPerCountryAuxClasses.Columns()
	# Se crea objeto con todos los paises conocidos
	while True: 
		if ans=="n": 
			print("\t\tExiting. ")
			break
		elif ans=="y":
			country = getCountry(countries)
			plot(country)
			ans = input("\n\tDo you want to plot another country? (y/n): ")
		else: 
			ans = input("\n\tInvalid input. Do you want to plot another country? (y/n): ")
	print("\tProcess finished. ")
