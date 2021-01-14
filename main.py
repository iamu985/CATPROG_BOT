import imaplib
import email
from mailparser import Parser
from record import Record
import json

class Gmail:
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.host = 'imap.gmail.com'
		self.mail = imaplib.IMAP4_SSL(self.host)
		self.parse = Parser()
		self.record = Record()
		self.keys = []
		
		#my database
		self.database = self.record.loader('m')
		self.iddata = {'id':self.keys}
		
	def run(self):
		#logging in to the gmail account
		ids_list = self.login()
		length = len(ids_list)
		if self.check_data(length):
			for i in range(len(self.database), length):
				#fetching raw_email
				print('IDS: ', ids_list[i])
				raw_email = self.generate_rawdata(i, ids_list)
				#check FROM has required keywords
				self.keys.append(str(ids_list[i]))
				self.storeID()
				self.record.generate(str(ids_list[i]), 'd', subject=raw_email['subject'],
							from_=raw_email['from'], time=raw_email['Received'], status='Checked')
				
				flag = self.parse.check_keywords(raw_email['from'])
				if flag:
					for part in raw_email.walk():
						#update the status to CHECKED
						self.record.generate(str(ids_list[i]), 'm', subject=raw_email['subject'],
							from_=raw_email['from'], time=raw_email['Received'], status='Checked')
						print(f'Recorded id {ids_list[i]}\n')
							
						#self.database[self.keys[-1]]['status']='CHECKED'
						if part.get_content_type() == 'text/plain':
							body = part.get_payload(decode=True).decode('utf-8')
							#swapping dear frank
							self.parse.swap_keywords(body)
							#check for urls
							self.parse.check_urls(body)



	def login(self):
		self.mail.login(self.username, self.password)
		self.mail.select('INBOX')
		status, data = self.mail.search(None, 'ALL')
		ids_list = data[0].split()
		return ids_list

	def generate_rawdata(self, idtag, ids_list):
		state, raw_data = self.mail.fetch(ids_list[idtag], '(RFC822)')
		raw_mail = raw_data[0][1]
		return email.message_from_string(raw_mail.decode('utf-8'))

	def check_data(self, idlength):
		if idlength > len(self.database):
			return True
		if idlength < len(self.database):
			return False
	
	def storeID(self):
		with open('id_data.json', 'w') as idfile:
			json.dump(self.iddata, idfile)




