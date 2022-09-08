from bs4 import BeautifulSoup
import requests
import re

class UserSite:

	def count_reader(self, user, flag):
		url = ''
		if flag == "stihi":
			url = 'https://stihi.ru/readers.html?'+user
		elif flag == "proza":
			url = 'https://proza.ru/readers.html?'+user
			
		html_text = requests.get(url).text
		soup = BeautifulSoup(html_text, 'lxml')
		quote = soup.select("p")[1]
		
		cleanr = re.compile('<.*?>')
		cleantext = re.sub(cleanr, '', str(quote))
		
		return cleantext
		
	def count_commets(self, user, flag):
		url = ''
		if flag == "stihi":
			url = 'https://stihi.ru/avtor/'+user
		elif flag == "proza":
			url = 'https://proza.ru/avtor/'+user
			
		html_text = requests.get(url).text
		soup = BeautifulSoup(html_text, 'lxml')
		
		quote = soup.select("#container > div.maintext > index > p > b:nth-child(4)")
		
		return quote[0].contents[0]