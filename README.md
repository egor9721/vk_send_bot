# VK_send_bot

# Описание приложения:

Данное приложение предназначено для массовой рассылки сообщений от имени сообщества. 
Ограничением на рассылку является, то что рассылка пройдет только по пользователям, разрешившим отправлять сообщения сообществу. 
Приложение работает локально на компьютере пользователя.

По итогу работы приложения будет выведена статистика по работе приложения:
* Количество пользователей, до которых дошло сообщение
* Количество пользователей, до которых сообщение не дошло
* Количество пользователей, аккаунт которых не существует
* Список пользователей с несуществующим аккаунтом
* Список пользователей, до которых сообщение не дошло


Добавление токенов сообщества осуществляется в файле config.py или через графический интерфейс

#Инструкция по работе с приложением:
1. после запуска приложения необходимо заполнить поля адресаты, сообщение и сообщество
2. поля адресаты и сообщение заполняются путем выбора файлов соответственно с адресатами, которым необходимо отправить сообщение и самим сообщением
3. В поле сообщество нужно выбрать сообщество от имени которого будет осуществляться рассылка
4. Если необходимо добавить новое сообщество для рассылки, то необходимо нажать кнопку добавить и ввести имя сообщества и его токен, предварительно полученный от ВК
5. после того как все поля будут заполнены, нажмите "Начать рассылку"
6. По окончании рассылки будет выведена статистика работы программы 

#Как получить токен сообщества:

Чтобы получить токен сообщества, необходимо зайти в настройки этого сообщества, выбрать раздел "Работа с API" и скопировать/создать ключ (у ключа должен быть доступ к сообщениям сообщества), после чего добавить полученныей токен в приложение.
