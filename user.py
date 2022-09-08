import pickle
from cryptography.fernet import Fernet
import os

class UserFile:
	FILENAME = "user.bin"
	CRYPTOFILE = 'crypto.key'

	def write_key(self):# создание ключа
		key = Fernet.generate_key()
		with open(self.CRYPTOFILE, 'wb') as key_file:
			pickle.dump(key, key_file)
			
	def load_key(self):# чтение и возвращение ключа из файла
		with open(self.CRYPTOFILE, 'rb') as file:
			key = pickle.load(file)
				
		return key

	def write_crypt(self):# шифрование файла
		try:
			key = self.load_key()
			
			f = Fernet(key)
			with open(self.FILENAME, 'rb') as file_read:
				file_data = file_read.read()
			
			encrypted_data = f.encrypt(file_data)
			
			with open(self.FILENAME, 'wb') as file_write:
				pickle.dump(encrypted_data, file_write)
				
		except FileNotFoundError:
			print("Ошибка при записи: Нет файла ключей или файла с данными пользователя!")
			
	def read_crypt(self):# расшифровка файла

		try:
			key = self.load_key()
			f = Fernet(key)
			
			with open(self.FILENAME, 'rb') as file_read:
				encrypted_data = pickle.load(file_read)
			
			decrypted_data = f.decrypt(encrypted_data)
			
			with open(self.FILENAME, 'wb') as file_write:
				file_write.write(decrypted_data)
				
		except FileNotFoundError:
			print("Ошибка при чтение: Нет файла ключей или файла с данными пользователя!")

	def write_data(self, user):# функция запипи в файл
		list = []
		if os.path.exists(self.FILENAME):
			list = self.read_data()
			
			
		list.append(user)
		with open(self.FILENAME, "wb") as file:
			pickle.dump(list, file)
			
		self.write_crypt()
		
		
	def read_data(self):# функия чтения из файла
		self.read_crypt()
		
		with open(self.FILENAME, "rb") as file:
			us = pickle.load(file)
			
		self.write_crypt()
		return us
	
	def creat_user(self):
		if not os.path.exists(self.CRYPTOFILE):
			self.write_key()
			print("Файл ключей успешно создан!\n")
			
		print("Введите:\n1 - Стихи\n2 - Проза")
		num = 0
		while True:
			num = int(input("-> "))
			if num in [1,2]:
				break;
		login = input("Ваш логин -> ").strip()
		password = input("Ваш пароль -> ").strip()
		self.write_data({"login":login, "password":password, "flag":['stihi','proza'][num-1]})
	
	def input_id_from_list(self, list_user):
		num_us = 0
		while True:
			num_us = abs(int(input("Введите цифру-> ")))
			if num_us <= len(list_user):
				num_us -= 1
				break
				
		return num_us
		
	def id_user_form_list(self, list_user):
		pace = {"stihi":'Стихи.ру',"proza":'Проза.ру'}
		for i in range(len(list_user)):
			print(str(i+1)+" - "+list_user[i]['login']+' на '+pace[list_user[i]['flag']])
				
		return self.input_id_from_list(list_user)
				
	def mod_user(self):
		list_user = self.read_data()
		id_user = self.id_user_form_list(list_user)
		print("1 - Изменить логин\n2 - Изменить пароль")
		
		num_chan = self.input_id_from_list([1,2])
		lis = {0:'login', 1:'password'}
		value = input("Новый "+lis[num_chan]+"-> ")
		list_user[id_user][lis[num_chan]] = value
		
		with open(self.FILENAME, "wb") as file:
			pickle.dump(list_user, file)
			
		self.write_crypt()
		
	def del_user(self):
		list_user = self.read_data()
		id_user = self.id_user_form_list(list_user)
		del list_user[id_user]
		
		with open(self.FILENAME, "wb") as file:
			pickle.dump(list_user, file)
			
		self.write_crypt()
		