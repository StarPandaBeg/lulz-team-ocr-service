import requests

# URL для POST-запроса
url = "http://127.0.0.1:5003/parseimg"

# Открываем файл в бинарном режиме
file = open("main.jpg", "rb")

# Создаем словарь для отправки файла
files = {"file": file}

# Отправляем POST-запрос с файлом
response = requests.post(url, files=files)

# Выводим ответ на консоль
print(response.text)

# Закрываем файл
file.close()
