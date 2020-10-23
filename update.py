# python /Users/sebastianmorales/Desktop/Prog/Python\ Projs/Coronavirus\ Data/update.py 

import auxsPkgs.infoPerCountry
import auxsPkgs.updateData

if __name__ == "__main__": 
	print(chr(27) + "[2J")
	def showCentered(text, nChars):
		if len(text)>nChars: 
			print(text[0:nChars])
			showCentered(text[(nChars+1):], nChars)
		else: 
			sideTabs = int((nChars - len(text))*0.5/8)
			remainingSideSpaces = int((nChars-len(text))*0.5 - 8 * sideTabs)
			print("\t"*sideTabs + " "*remainingSideSpaces + text + " "*remainingSideSpaces + "\t"*sideTabs)
	print("\n"*2)
	nChars = 150
	title = "GETTING DATA FROM COVID-19 AROUND THE WORLD"
	showCentered(title, nChars)
	showCentered("="*(len(title)+10), nChars)
	showCentered("Data extracted from worldometers.info", nChars)
	showCentered("Made by Sebastian M. - smoralesarueste@gmail.com", nChars)
	print("\n")
	auxsPkgs.updateData.updateData()
	print("\n")
	auxsPkgs.infoPerCountry.updateData()
	print("\n")
	print("="*nChars)
	print("="*nChars+"\n")
	showCentered("Process finished. Data has been stored. ", nChars)
	showCentered("="*(len(title)+10), nChars)
	showCentered("Program finished. ", nChars)
	print("\n")
