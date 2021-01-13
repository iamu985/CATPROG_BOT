


#check for new emails
#----how to do that (by comparing the last id from the local database 
#----with the recent id
#----if true then fetch the last id from the database and collect all the 
#----mails from the last entry to the recent entry
#Then pass it through the parser to record any new query related announcements
#create a short messages from the announcements

class Run:
	def __init__(self, mail, setup, idslist):
		self.mail = mail
		self.setup = setup
		self.idslist = idslist
		self.lengthLocal = len(self.setup.idbase)
		self.lengthRecent = len(self.idslist) 
		
	def __call__(self):
		print('Ran')
		for i in range(self.lengthLocal, self.lengthRecent):
			raw_mails = self.mail.generate_rawdata(i, self.idslist)
			
			#storing new ids in the idbase file
			self.setup.idbase.append(str(self.idslist[i]))
			self.appendID(self.setup.idbase)
			
			#storing new emails in databasefile
			self.setup.record.generate(str(self.idslist[i]),'d',subject=raw_mails['subject'],
			from_=raw_mails['from'],time=raw_mails['Received'],status='DENIED')
			
			#checking if the mails contain the required keywords or not
			if self.setup.parse.check_keywords(raw_mails['from']):
				#parsing the mails to create a message
				for part in raw_mails.walk():
					#new mails to be stored in mailbase file
					self.setup.record.generate(str(self.idslist[i]),'m',subject=raw_mails['subject'],
					from_=raw_mails['from'],time=raw_mails['Received'],status='CHECKED')
					
					if part.get_content_type() == 'text/plain':
						body = part.get_payload(decode=True).decode('utf-8')
						
						#swapping the keywords
						self.setup.parse.swap_keywords(body)
						
						#check for urls
						self.setup.parse.check_urls(body)
	
	def appendID(self, idbase):
		#appends new id to the idbasefile
		with open(self.setup.idbasefile, 'w') as appendObj:
			json.dump(self.setup.idbase, appendObj)
			
		
		
			 
		
		
