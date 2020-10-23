# python /Users/sebastianmorales/Desktop/Otros/Coronavirus\ Data/historicWebPage.py

import auxsPkgs.auxsInternet
from auxsPkgs.auxsDateTimeMoment import Date, Time, Moment
import datetime
import sys

# Clase que obtiene todos los snapshots disponibles para cierta pagina web, entre las dos fechas indicadas
# Busca la info en webarchive.org
class HistoricWebPage:
	def __init__(self, url, tInit, tFinal): 
		self.url = auxsPkgs.auxsInternet.URL(url)
		self.window = (tInit, tFinal)
		self.moments = self.getMoments()
		self.snapshots = None
	# Busca en que fechas, dentro del margen indicado, existen cambios
	def getDates(self):
		years = [self.window[0].year+i for i in range(self.window[1].year - self.window[0].year + 1)]
		totalDates = []
		nUpdates = 0
		for year in years: 
			path = "https://web.archive.org/__wb/calendarcaptures/2?url=" + self.url.url + "%2F&date=" + str(year) + "&groupby=day"
			content = auxsPkgs.auxsInternet.Web_Connection(path).html.clean()
			if content=="{}": continue
			_locals = locals()
			exec("D=dict("+content+")", _locals)
			items = _locals["D"]["items"]
			nDates = len(items)
			dates = []
			for i in range(nDates):
				date = items[i][0]
				month = int(date/100)
				day = int(date - 100 * month)
				date = Date(day, month, year)
				if ((date >= self.window[0]) & (date <= self.window[1])):
					nUpdates += items[i][2]
					dates+=[date]
			totalDates+=dates
		return totalDates, nUpdates
	# Busca a que horas de cada fecha encontrada, se hicieron los cambios
	def getMoments(self):
		dates, nUpdates = self.getDates()
		moments = []
		D = dict()
		_locals = locals()
		k = n = 0
		for i in range(len(dates)): 
			date = dates[i]
			path = ("https://web.archive.org/__wb/calendarcaptures/2?url=" + self.url.url + "%2F&date=" 
				+ "".join(str(date).split("/")[::-1])
				)
			content = auxsPkgs.auxsInternet.Web_Connection(path).html.clean()
			exec("D=dict("+content+")")
			updates = _locals["D"]["items"]
			nMoments = len(updates)
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
				moments += [Moment(date, Time(hour, minute, second))]
		return moments
	# Busca el snapshot de la pagina en la hora-dia encontrada
	def getSnapshot(self, moment):
		path = ("https://web.archive.org/web/" + 
				"".join(str(moment.date).split("/")[::-1]) + 
				str(moment.time).replace(":","")+ 
				"/https://www.worldometers.info/coronavirus/")
		return auxsPkgs.auxsInternet.Web_Connection(path)
	def getSnapshots(self):
		D = dict()
		show = False
		nMoments = len(self.moments)
		for i in range(nMoments):
			moment = self.moments[i]
			if i==0: 
				t0 = datetime.datetime.now()
			path = ("https://web.archive.org/web/" + 
				"".join(str(moment.date).split("/")[::-1]) + 
				str(moment.time).replace(":","")+ 
				"/https://www.worldometers.info/coronavirus/")
			D[moment] = auxsPkgs.auxsInternet.Web_Connection(path)
			if i==0: 
				tf = datetime.datetime.now()
				secs = (tf-t0).total_seconds()
				if (secs*nMoments > 30): 
					show = True
			if show:
				showProgress(i, nMoments)
		self.snapshots = D

# Funcion que genera barra de progreso cuando se han hecho n tareas de un total de N
def showProgress(n,N,nDec = 1): 
	def getDec(x,k): 
		trunc = int(x/(10**k))
		return int(trunc - 10*int(trunc/10))
	progress = (n+1)/N
	decs = [getDec(progress, -(i+1)) for i in range(nDec+2)]
	if n>0:
		sys.stdout.write("\033[F")
		sys.stdout.write("\033[K")
	if progress<0.1:
		print("="*25 + " " + str(decs[1]) + "." + str("".join([str(decs[i+2]) for i in range(nDec)])) + " % " + "="*25)
	elif progress<1:
		print("="*25 + " " + str(getDec(progress,-1)) + str(getDec(progress,-2)) + "." + str("".join([str(decs[i+2]) for i in range(nDec)])) + " % " + "="*25)
	else:
		print("="*25 + " COMPLETED " + "="*25)










