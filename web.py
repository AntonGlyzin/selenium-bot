from selenium import webdriver
import datetime
import time
from selenium.common.exceptions import WebDriverException
import re
from pars import UserSite
import random
from ini import IniWork

class WebSite:
	
	def __init__(self, lgn, pswd, flag):
		self.DAY = str(datetime.datetime.now().day)
		self.MON = str(datetime.datetime.now().strftime("%m"))
		self.YEAR = str(datetime.datetime.now().strftime("%Y"))
		
		self.NAME = lgn
		self.PASSWORD = pswd
		
		self.FLAG = flag
		
		if flag == "stihi":
			self.LOGIN_LINK = 'https://stihi.ru/login/'
			self.DOM_SITE = 'Стихи.ру'
			self.XPATH_COUNT = '//*[@id="container"]/div[2]/index/p[2]'
			self.XPATH_RAZDEL = '//*[@id="container"]/div[2]/index/h1'
		elif flag == "proza":
			self.LOGIN_LINK = 'https://proza.ru/login/'
			self.DOM_SITE = 'Проза.ру'
			self.XPATH_COUNT = "/html/body/div/table/tbody/tr/td/index/p[2]"
			self.XPATH_RAZDEL = '/html/body/div/table/tbody/tr/td/index/h1'
		
		
		self.DRIV = webdriver.Chrome()
		self.DRIV.implicitly_wait(10)
		
	def input_site(self):
		self.DRIV.get(self.LOGIN_LINK)
		username_input = self.DRIV.find_element_by_css_selector("input[name='login']")
		password_input = self.DRIV.find_element_by_css_selector("input[name='password']")

		username_input.send_keys(self.NAME)
		password_input.send_keys(self.PASSWORD)

		self.DRIV.find_element_by_css_selector("input[type='submit']").click()
		
	def write_log(self, text):
		if self.FLAG == "proza":
			file = open("log-proz.txt",'a')
		elif self.FLAG == "stihi":
			file = open("log-stih.txt",'a')
			
		file.write(text)
		file.close()
		
	def write_links_to_file(self,year, month, beg_day=1, counts_day=1):
	
		count_lnk = 0
		with open('pageslnk{m}.txt'.format(m=month),'w') as file:
			print("|======= Loading links to file... ======|\n")
			
			for day in range(beg_day,counts_day+1):
				self.DRIV.get("https://stihi.ru/poems/list.html?topic=01&year={year}&month={month}&day={day}".format(year=year, month=month, day=day))
				
				pages_lnk = self.DRIV.find_elements_by_xpath("/html/body/div/div[2]/index/div[3]/a")
				
				for page_lnk in pages_lnk:
					file.write(page_lnk.get_attribute('href')+"\n")
					count_lnk += 1
					print("| "+str(count_lnk) + " links is downloaded from {d} day...".format(d=day), end="\r")
			print("\n| All links is downloaded\n")
			print("\n|=======================================|")
			
	def del_links_file(self,name_file):
		ini_file = IniWork()
		del_count = ini_file.read_ini("Links","count")
		
		if int(del_count) != 0:
			with open(name_file,'r') as file:
				lines = file.readlines()
				for line in range(int(del_count)):
					lines.pop()
				ini_file.update_ini("Links","count", str(0))
				
			with open(name_file,'w') as file:	
				file.writelines(lines)
			
				
			
	def start_bot_v4(self,name_file):
		
		try:
			with open(name_file,'r') as file:
				lines = file.readlines()
				
			print("|======= Program is begin working... ======|")
			print("| {n} links in the file\n".format(n=len(lines)))
			
			view_count = 0
			view_count_link = 0
			ini_file = IniWork()
			for lnk in lines[::-1]:
				time.sleep(3)
				self.DRIV.get(lnk)
				
				view_count_link += 1
				ini_file.update_ini("Links","count", str(view_count_link))
				
				arr01 = self.DRIV.find_elements_by_xpath("/html/body/div/div[2]/index/ul[1]/li/a")
				arr02 = self.DRIV.find_elements_by_xpath("/html/body/div/div[2]/index/ul[2]/li/a")
				
				lnk_poems = []
				for arr_ul in [arr01,arr02]:
					for arr in arr_ul:
						lnk_poems.append(arr.get_attribute('href'))
						
				
				print("|-"+str(view_count_link) + " view of links...            ")		
				for lnk_poem in lnk_poems:
					time.sleep(3)
					self.DRIV.get(lnk_poem)
					view_count += 1
					print("|---"+str(view_count) + " viewed poems", end="\r")
					time.sleep(9)
					self.DRIV.back()
					
			self.del_links_file(name_file)
			
			print("\n\n|================= END ====================|")
		except :
			self.del_links_file(name_file)
			print("\n\n|================= END ====================|")
		
	def start_bot_v3(self, month, day):	
		
		self.DRIV.get("https://stihi.ru/poems/list.html?topic=01&year=2021&month={month}&day={day}".format(month=month, day=day))
		pages_lnk = self.DRIV.find_elements_by_xpath("/html/body/div/div[2]/index/div[3]/a")
			
		arr_page_lnk = []
		print("|=========== day is {d} ==============|".format(d=day))
		print("Loading links of pages...\n")
			
		count_lnk = 0
		for lnk in pages_lnk:
			if count_lnk == (len(pages_lnk)-1):
				break
					
			arr_page_lnk.append(lnk.get_attribute('href'))
			count_lnk += 1
			print(str(count_lnk)+" out of "+str(len(pages_lnk))+" links is loaded...", end="\r")
				
		print("\nLinks is loaded.\n")
		print("======================================")
			
		view_count = 0
		for lnk in arr_page_lnk[::-1]:
			time.sleep(3)
			self.DRIV.get(lnk)
			
			arr01 = self.DRIV.find_elements_by_xpath("/html/body/div/div[2]/index/ul[1]/li/a")
			arr02 = self.DRIV.find_elements_by_xpath("/html/body/div/div[2]/index/ul[2]/li/a")
				
				
			lnk_poems = []
			for arr_ul in [arr01,arr02]:
				for arr in arr_ul:
					lnk_poems.append(arr.get_attribute('href'))
						
			for lnk_poem in lnk_poems:
				time.sleep(3)
				self.DRIV.get(lnk_poem)
				view_count += 1
				print(str(view_count) + " viewed poems...", end="\r")
				time.sleep(9)
				self.DRIV.back()

		
		
	def start_bot_v2(self):
		self.input_site()
		self.DRIV.get('https://stihi.ru/authors/online.html')
		elem_auth = self.DRIV.find_elements_by_xpath("//a[@class='recomlink']")
		arr_lnk = []
		print("Loading links...\n")
		
		count_lnk = 0
		for lnk in elem_auth:
			arr_lnk.append(lnk.get_attribute('href'))
			count_lnk += 1
			print(str(count_lnk)+" out of "+str(len(elem_auth))+" links is loaded.", end="\r")
			
		print("\nLinks is loaded.\n")	
		
		view_count = 0
		for lnk in arr_lnk[::-1]:
			time.sleep(3)
			self.DRIV.get(lnk)
			
			elem_lnk = self.DRIV.find_elements_by_xpath("//a[@class='poemlink']")
			if len(elem_lnk) > 3:
				elem_lnk[random.randint(0, len(elem_lnk)-1)].click()
				view_count += 1
				print(str(view_count)+" out of "+str(count_lnk)+" viewed links...", end="\r")
				time.sleep(9)
				self.DRIV.back()
			
			self.DRIV.back()
			
		self.DRIV.quit()
			
	def start_bot(self, link):
		self.input_site()
		self.DRIV.get(link)
		
		xpat_text = self.DRIV.find_elements_by_xpath(self.XPATH_COUNT)[0].text
		old_count = int(re.findall('[0-9]+', xpat_text)[0])
		
		razd_text = " ".join(self.DRIV.find_elements_by_xpath(self.XPATH_RAZDEL)[0].text.split()[1:])
		
		print(self.DAY+"."+self.MON+"."+self.YEAR+": "+str(old_count)+" - количество записей на сайте "+self.DOM_SITE+" "+razd_text)
		
		all_count = 0
		try:
			while True:
				time.sleep(10)
				self.DRIV.get(link)	
				
				new_count_text = self.DRIV.find_elements_by_xpath(self.XPATH_COUNT)[0].text
				new_count = int(re.findall('[0-9]+', new_count_text)[0])
				if old_count < new_count:
					self.DRIV.get(self.DRIV.find_elements_by_xpath("//ul[@type='square']/li/a")[0].get_attribute('href'))
					all_count += 1
					print("----- "+str(new_count)+" - количество записей на сайте. | Из них просмотренно - "+str(all_count))
					old_count = new_count
					time.sleep(3)
					self.DRIV.get(link)
					
				
		except :
			
			usr_site = UserSite()
			count_read = usr_site.count_reader(self.NAME, self.FLAG)
			count_comm = "Всего рецензий - "+usr_site.count_commets(self.NAME, self.FLAG)
			
			print("Просмотренно "+str(all_count)+" записей.\n"+count_read+"\n"+count_comm)
			
			self.write_log(self.DAY+"."+self.MON+"."+self.YEAR+": "+str(all_count)+" - количество записей просмотренно из "+razd_text+"\n"+count_read+". "+count_comm+"\n")
			self.DRIV.quit()
		