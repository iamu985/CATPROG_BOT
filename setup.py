from main import Gmail
import json
from dtime import TimeCheck
from record import Record
from run import Run

#get the last id from the database
#get the last id entry from email
#compare time between those emails
#if the time is similar or equal then stop the script
#if the time is greater then run the script

###SCRIPT####
#Run Gmail from main
#logs in to the gmail account using imap
#get all the email from the last id of the local database to the 
#latest entry of the email
#check if recent email fit the parsers requirement
#if it does then store the email to the local database
#create a message
#sent it to the bot
#the bot sends the message
###############################################################

class Setup:
	def __init__(self):
		self.username = ''
		self.password = ''
		self.maildatafile = 'mail_data.json'
		self.databasefile = 'database.json'
		self.idbasefile = 'id_data.json'
		
		self.mail = Gmail(self.username, self.password)
		self.record = Record()
		self.timecheck = TimeCheck()
		
		self.database = self.record.loader('d')
		self.mailbase = self.record.loader('m')
		self.idbase = self.record.loader('i')['id']
	
	def __call__(self):
		idlist = self.mail.login()
		recentID = idlist[-1]
		lastID = self.idbase[-5]
		
		runscript = Run(self.mail, self, idlist)
		#getting time from recent id
		recentMail = self.mail.generate_rawdata(-1, idlist)
		
		#times
		recentTime = self.timecheck.formatTime(recentMail['Received'])
		lastTime = self.timecheck.formatTime(self.database[str(lastID)]['time'])
		
		flag = self.timecheck.compare(recentTime, lastTime)
		print(f'Flag: {flag}')
		if flag:
			runscript()
		else:
			print('No new messages')
			#terminating the script
			pass

setup = Setup()
setup()
