import datetime

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
	def __ge__(self,date2):
		return ((self>date2) | (self==date2))
	def __le__(self,date2):
		return ((date2>self) | (self==date2))
	def __hash__(self):
		return hash((self.day, self.month, self.year))
	def todatetime(self): 
		return datetime.date(self.year, self.month, self.day)


# Objetos que guardan hora - minuto
# Pueden transformarse a string en formato hh:mm
# self.dayProgress devuelve numero en (0,1) segun cuanto tiempo del dia ha avanzado
# Puede utilizar desigualdades
class Time: 
	def __init__(self, hour, minute, second): 
		self.hour = hour
		self.minute = minute
		self.second = second
		self.dayProgress = (self.hour/24.0) + (self.minute/(60.0*24.0)) + (self.second/(60.0*60.0*24.0))
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
	def __hash__(self):
		return hash((self.hour,self.minute,self.second))
	def todatetime(self): 
		return datetime.time(self.hour, self.minute, self.second)

# Objeto que guarda fecha - hora
# Puede utilizar desigualdades
#  Pueden transformarse a string en formato mm:hh dd/mm/yyyy
class Moment: 
	def __init__(self, date, time): 
		self.date = date
		self.time = time
	def __gt__ (self, moment2): 
		if self.date > moment2.date: 
			return True
		elif self.date == moment2.date: 
			return self.time > moment2.time
		return False
	def __lt__ (self, moment2): 
		return moment2 > self
	def __ge__ (self, moment2):
		return ((self>moment2) | (self==moment2))
	def __le__ (self, moment2):
		return moment2>=self
	def __eq__ (self, moment2): 
		return ((self.time == moment2.time) & (self.date == moment2.date))
	def __str__ (self): 
		return str(self.date) + " " + str(self.time)
	def __hash__(self):
		return hash((self.date, self.time))
	def pathString(self): 
		return self.date.pathString() + " " + self.moment.pathString()
	def todatetime(self): 
		return datetime.datetime(self.date.year, self.date.month, self.date.day, self.time.hour, self.time.minute, self.time.second)





