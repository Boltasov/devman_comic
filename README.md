'''
Get token

https://oauth.vk.com/blank.html#access_token=&expires_in=86400&user_id=275658820
'''
# Публикация комиксов

Программа предназначена для публикации комиксов с сайта https://xkcd.com/ в группе Вконтакте.

### Как установить

Должны быть предустановлены Python 3 и pip.

Скачайте код с помощью команды в командной строке
```
git clone https://github.com/Boltasov/devman_comic
```
Установите необходимые библиотеки командой
```
python pip install -r requirements.txt
```
Для запуска кода понадобится:

- Создать собственное приложение во [Вконтакте](https://vk.com/dev). В качестве типа приложения следует указать standalone. 
- Получить `client_id` этого приложения. Для этого нажмите кнопку "Редактировать" на странице "Мои приложения". В адресной строке вы увидите `client_id` приложения. Скопируйте и сохраните его.
- Получить ключ доступа. Для этого сделайте приведённый ниже запрос в браузер, предварительно вставив в url полученный ранее client_id:
- Получить `group_id` для вашего паблика. Откройте страницу паблика. В вдресной строке вы увидите цифры после `https://vk.com/club`. Это ваш `group_id`. Скопируйте и сохраните его.
```
https://oauth.vk.com/authorize?client_id=[YOUR_CLIENT_ID]&redirect_uri=https://oauth.vk.com/blank.html&scope=photos,groups,wall&response_type=token
```

Создайте в той же папке, где находится `main.py` новый файл с названием `.env`. Вставьте в него следующие данные:
```
VK_APP_CLIENT_ID=[YOUR_CLIENT_ID]
VK_ACCESS_TOKEN = ['YOUR_TOKEN']
VK_API_VERSION=5.131
VK_GROUP_ID=[YOUR_GROUP_ID]
```

Теперь, чтобы запустить код, используйте команду:
```commandline
python main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).