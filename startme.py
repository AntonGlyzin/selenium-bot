import sys
import os
from user import UserFile
from web import WebSite
from ini import IniWork
from pars import UserSite

if __name__ == "__main__":
	user = UserFile()
	if not os.path.exists(user.FILENAME) and not os.path.exists(user.CRYPTOFILE):
		user.creat_user()
	elif not os.path.exists(user.CRYPTOFILE):
		print("Ошибка: Нет файла ключей!")
		input()
		sys.exit()
	elif not os.path.exists(user.FILENAME):
		print("Ошибка: Нет файла с пользователями!")
		input()
		sys.exit()
	elif 'newUser' in sys.argv:
		user.creat_user()
	elif 'modUser'  in sys.argv:
		user.mod_user()
	elif 'delUser'  in sys.argv:
		user.del_user()
	elif 'cmd'  in sys.argv:
		print("newUser, modUser, delUser, fileLinks") #write_links_to_file(self,year, month, beg_day=1, counts_day=1) 2021 12 1 30
		sys.exit()
		
	list_user = user.read_data()
	print("В программе зарегистрировано "+ str(len(list_user)) + " пользователя" if len(list_user)>1 else 'В программе зарегистрирован 1 пользователь')
	
	num_us=0
	if len(list_user)>1:
		num_us = user.id_user_form_list(list_user)
		
	
	os.system('cls' if os.name=='nt' else 'clear')
	web = WebSite(list_user[num_us]["login"],list_user[num_us]["password"],list_user[num_us]["flag"])
	ini_file = IniWork()
	
	if web.FLAG == "stihi":
		web.input_site()
		
		if 'fileLinks'  in sys.argv:
			web.write_links_to_file(str(sys.argv[2]),str(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]))
			web.DRIV.quit()
			sys.exit()
		
		name_file = ini_file.read_ini("Links","file")
		name_file += '.txt'
		
		web.del_links_file(name_file)
		web.start_bot_v4(name_file)
		web.DRIV.quit()
	
		
		
		