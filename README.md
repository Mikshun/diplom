# Бот для поиска ресторанов
## Описание
Данный бот предназначен для поиска ресторанов, в любой точке мира. Используя интеграцию с внешним Api [The Fork The Spoon](https://rapidapi.com/apidojo/api/the-fork-the-spoon/),
написанным на Python.
## Команды бота
В боте рализовано 4 команды:
+ `/low` - вывод самых дешевых ресторанов в выбранном городе
+ `/high` - вывод самых дорогих ресторанов в выбранном городе
+ `/custom` - вывод ресторанов с настраиваемыми пользователем параметрами
+ `/history` - вывод истории поиска пользователя
+ `/help` - вывод всех команд
## Примеры работы команд:
![example1](https://github.com/Mikshun/telebot_restaurants/blob/master/example_images/img.png)

![example2](https://github.com/Mikshun/telebot_restaurants/blob/master/example_images/img_1.png)

![example3](https://github.com/Mikshun/telebot_restaurants/blob/master/example_images/img_2.png)

![example4](https://github.com/Mikshun/telebot_restaurants/blob/master/example_images/img_3.png)

## Установка и Запус
+ Скачать репозиторий можно при помощи команды:
  ```bash 
  git clone https://github.com/Mikshun/telebot_restaurants
  ```
+ Перейти в папку проекта и создать файл `.env` шаблон файла описан в файле `.env.template`
+ Запустить файл main.py
