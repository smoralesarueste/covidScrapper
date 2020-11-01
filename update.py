# python /Users/sebastianmorales/Desktop/Prog/Python\ Projs/Coronavirus\ Data/update.py 

import auxsPkgs.infoPerCountry
import auxsPkgs.updateData
import auxsPkgs.plotCreator
import os

if __name__ == "__main__": 
	print("\n"*2)
	def showCentered(text, nChars):
		if len(text)>nChars: 
			print(text[0:nChars])
			showCentered(text[(nChars+1):], nChars)
		else: 
			sideTabs = int((nChars - len(text))*0.5/8)
			remainingSideSpaces = int((nChars-len(text))*0.5 - 8 * sideTabs)
			print("\t"*sideTabs + " "*remainingSideSpaces + text + " "*remainingSideSpaces + "\t"*sideTabs)
	print("\n"*2)
	dims = os.get_terminal_size()
	title = "GETTING DATA FROM COVID-19 AROUND THE WORLD"
	showCentered(title, dims[0])
	showCentered("="*(len(title)+10), dims[0])
	showCentered("Data extracted from worldometers.info", dims[0])
	showCentered("Made by Sebastian M. - smoralesarueste@gmail.com", dims[0])
	print("\n")
	auxsPkgs.updateData.updateData()
	print("\n")
	auxsPkgs.infoPerCountry.updateData()
	print("\n")
	auxsPkgs.plotCreator.plotCountry()
	print("\n")
	print("="*dims[0])
	print("="*dims[0]+"\n")
	showCentered("Process finished. Data has been stored. ", dims[0])
	showCentered("="*(len(title)+10), dims[0])
	showCentered("Program finished. ", dims[0])
	print("\n")
