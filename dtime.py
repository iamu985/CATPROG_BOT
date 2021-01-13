import datetime
import json
import time
from record import Record


class TimeCheck:
	def __init__(self):
		self.monthConversionMap = {
		'Jan':1,
		'Feb':2,
		'Mar':3,
		'Apr':4,
		'May':5,
		'Jun':6,
		'Jul':7,
		'Aug':8,
		'Sep':9,
		'Oct':10,
		'Nov':11,
		'Dec':12,
		}
	
	def compare(self, dnow, ddata):
		#compare datetimes
		if dnow > ddata:
			return True #returns true if current time is greater than the last 
		if dnow < ddata:
			return False
	
	
	def formatTime(self, timestring):
		datetimeObj = timestring.split()[6:11]
		timeObj = datetimeObj[4].split(":")
		stringFormatted = ''.join(datetimeObj[0]+(datetimeObj[1])+','+datetimeObj[2]+','+(datetimeObj[3])+
						  ','+(timeObj[0])+':'+(timeObj[1])+':'+(timeObj[2]))
		time_string = stringFormatted.split(',')
		#converting into month
		time_string[2] = self.monthConversionMap[time_string[2]]
		
		#current datetime
		datetimeData = datetime.datetime(int(time_string[3]), int(time_string[2]),
									 int(time_string[1]), int(timeObj[0]),
									 int(timeObj[1]),int(timeObj[2]))
		return datetimeData
		
