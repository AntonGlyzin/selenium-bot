# selenium-bot

Специальный скрипт для прохода ссылок от лица автора на сайте стихотворений.
При первом запуске следует создать пользователя, указав свой логин и пароль. Программа зашифрует эти данные и создаст ключ для открытия этого файла. Файл будет расшифровываться каждый раз при включение программы, а после получения логина и пароля зашифровываться.
Но перед началом работы нужно будет создать файл с ссылками. Для этого есть специальная команда с выбором интервала парсинга.
После того как список ссылок получен, можно запускать программу. Программа будет получать ссылку из файла, заходить на нее, и ввести счет просмотренных ссылок. При следующем запуске просмотренные ссылке будут удаленны, а программу будет идти по новым ссылкам в файле.
