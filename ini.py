import configparser
import os

class IniWork:

	def __init__(self):
		self.INIFILE = 'config.ini'
		self.CONF = configparser.ConfigParser()
		
		if os.path.exists(self.INIFILE):
			self.CONF.read(self.INIFILE)
		
	def read_ini(self, sect, key):
		return self.CONF.get(sect, key)
		
	def update_ini(self, sect, key, val):
		self.CONF.set(sect, key, val)
		with open(self.INIFILE, "w") as conf_file:
			self.CONF.write(conf_file)