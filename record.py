import pandas as pd
import json

class Record:
	def __init__(self):
		self.args = ['subject', 'from_', 'time', 'status']
		self.data = {}
		self.datafile = 'mail_data.json'
		self.databasefile = 'database.json'
		self.idfile = 'id_data.json'
	
	def generate(self, idindex, cmd, **ext):
		for keys in ext.keys():
			if keys in self.args:
				self.data[idindex]=ext
		db = self.create_data()
		self.writer(db, cmd)
	
	def create_data(self):
		df = pd.DataFrame(self.data, columns=[i for i in self.data.keys()])
		return df
	
	def writer(self, database, cmd):
		if cmd == 'm':
			with open(self.datafile, 'w') as writeObj:
				json.dump(database.to_json(orient='columns'), writeObj)
				#print(f'File written to {self.datafile}')
		elif cmd == 'd':
			with open(self.databasefile, 'w') as writeObj:
				json.dump(database.to_json(orient='columns'), writeObj)
				#print(f'File written to {self.datafile}')
		if cmd != 'm' and cmd != 'd':
			print('Error: Invalid Command use m or d')
	
	def loader(self, cmd):
		if cmd == 'm':
			with open(self.datafile) as loadObj:
				return eval(json.load(loadObj))
		elif cmd == 'd':
			with open(self.databasefile) as loadObj:
				return eval(json.load(loadObj))
		elif cmd == 'i':
			with open(self.idfile) as loadObj:
				return json.load(loadObj)
		if cmd != 'm' and cmd != 'd' and cmd != 'i':
			print('Error: Invalid Command, pass m, i or d')
	
	def change_status(self, idtag, status):
		data = self.loader()
		cols = [key for key in data.keys()]
		df = pd.DataFrame(data, columns=cols)
		df[str(idtag)]['status'] = status
		self.writer(df)
	
	def reset(self):
		with open(self.datafile, 'w') as resetObj:
			df = pd.DataFrame(self.data)
			json.dump(df.to_json(), resetObj)

if __name__ == '__main__':
	record = Record()
	record.reset()
		

