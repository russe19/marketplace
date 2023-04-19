# Проект интернет-магазина
Командный проект интернет магазина.
1. [Описание](#introduction)
2. [Подготовка проекта к работе](#paragraph1)
    1. [Установка](#subparagraph1)
    2. [Запуск](#subparagraph2)
3. [Обзор](#paragraph2)
    1. [Основная информация](#subparagraph3)
    2. [Тесты](#subparagraph4)
    3. [API](#subparagraph5)
    4. [Транзакции](#subparagraph6)
    5. [Локализация и интернационализация](#subparagraph7)
    6. [Логирование](#subparagraph8)
    7. [Фикстуры и база данных](#subparagraph9)
    8. [Front-end](#subparagraph10)
## Описание <a name="introduction"></a>
В данном проекте реализован интернет-магазин по продаже электроники и техники, 
проект разрабатывался командой из 5 человек под руководством тимлида.
## Задачи, реализованные в проекте <a name="paragraph1"></a>
В процессе разработки проекта, для каждого участника были определены задачи, в список моих задачи входило:
- Создание модели и детальной страницы продавцов
- Создание модели и разработка детальной страницы товара
- Создание модели заказов и оформление заказа
- Разработка страницы «История заказов» и детальной страницы истории заказов
- Локализация сайта в админке, бэкенде и верстке
- Разработка верхнего меню и футера
В данном руководстве я подробно покажу результат проделанной мною работы, весь исходный код доступен в репозитории, 
в соответствующих местах я оставлю пути, для удобного поиска файлов с исходным кодом проекта.
### Создание модели и детальной страницы продавцов и товаров<a name="subparagraph4"></a>
![image](https://user-images.githubusercontent.com/116742525/233162926-4b068b4a-0473-4ca9-99c6-3d574f23617b.png)

[[https://user-images.githubusercontent.com/116742525/233164100-bad26a0a-4836-430f-8f56-df5d59ad9d87.png)|width=100px]]
<img src="![image](https://user-images.githubusercontent.com/116742525/233164100-bad26a0a-4836-430f-8f56-df5d59ad9d87.png)" width="100" height="100">
<img src="https://user-images.githubusercontent.com/116742525/233164100-bad26a0a-4836-430f-8f56-df5d59ad9d87.png" width="700" height="500">

![image](https://user-images.githubusercontent.com/116742525/233164163-05cc7da1-2339-44a9-9617-63cb9b3eb869.png)

![image](https://user-images.githubusercontent.com/116742525/233164333-c6d18f5f-916e-48ed-8635-ce215060ad4d.png)

![image](https://user-images.githubusercontent.com/116742525/233164749-021e0200-94ff-4fa8-80e8-2050745eb854.png)

![image](https://user-images.githubusercontent.com/116742525/233165086-15aa602f-569d-4fb4-b624-2ca103b66c66.png)

![image](https://user-images.githubusercontent.com/116742525/233165193-3aca37e7-c310-44e5-b2b9-195a60a2e966.png)
![image](https://user-images.githubusercontent.com/116742525/233165271-20b35524-8f0a-4671-a784-bb67d52e06d8.png)
![image](https://user-images.githubusercontent.com/116742525/233165327-52cc33b3-16f3-422b-9ea4-1426a7b8fd2b.png)
![image](https://user-images.githubusercontent.com/116742525/233165529-61849ea4-307f-4a34-9de4-ae7f6593d344.png)
![image](https://user-images.githubusercontent.com/116742525/233165581-9149c9fe-3326-4490-85eb-14c0d3564f65.png)
![image](https://user-images.githubusercontent.com/116742525/233166180-aac29eac-2897-41ad-b503-0ccaa0f7f0d6.png)
![image](https://user-images.githubusercontent.com/116742525/233166354-2843a227-e64b-449c-b035-31c382dea2c3.png)

В этом пункте, я подстраивал marketplace/product/templates/product/
На хостовую (основную) операционную систему необходимо установить:
- Oracle VM virtual box (возможно понадобится VPN)
- Vagrant (возможно понадобится VPN)
- Pycharm Pro (промокод запросить в службе поддержки студентов)
### Создание виртуальной машини vagrant
1. Запустить окно Oracle VM virtual box
2. В директории проекта запустить консольную команду ```vagrant up```
3. Сразу (не дожидаясь выполнения п.2) переключиться в окно Oracle VM virtual box. Сделать активной создаваемую виртуальную машину (дополнительных окон открывать не надо, просто нажать мышкой один раз)
> первый запуск может длиться 15-20 минут
> во время первого запуска следите, чтобы компьютер не переходил в "сон"
> возможно для первого запуска понадобится VPN
### Управление виртуальной машиной vagrant
* зайти в виртуальную машину
```commandline
vagrant ssh
```
* перезапустить виртуальную машину
```commandline
vagrant reload
```
* выключить виртуальную машину
```commandline
vagrant halt
```
* запустить скрипт установки ПО на виртуальную машину. Скрипт находится в папке `vagrant/provisioning/playbook.yml`. Запускается автоматически при первом выполнении `vargant up`. Эта команда может понадобится только на этапах настройки ВМ.
```commandline
vagrant provision
```
### Работа с проектом внутри локальной машины
* активация виртаульного окружения
```commandline
. ~/venv/bin/activate
```
* перейти в папку проекта
```commandline
cd /vagrant
```
* запустить проект (в папке проекте и внутри активированного виртуального окружения). На хостовой машине проект будет доступен по адресу [http://localhost:8181](http://localhost:8181)
```commandline
python manage.py runserver 0.0.0.0:8181
```
### Настройка интерпретатора для PyCharm Pro
#### Настройка интерпретатора  
В настройках IDE в пункте Project/Python Interpreter добавить интерпретатор Vagrant.  
Путь `/home/vagrant/venv/bin/python` 
#### Запуск сервера разработки  
В *Run/Debug Configurations* добавить Django Server  
host = 0.0.0.0  
port = 8181  
Run Browser http://localhost:8181/  
#### Запуск модульных тестов  
В *Run/Debug Configurations* добавить Django Tests с параметрами по умолчанию
#### Подключение к базе данных  
Через меню *Help/Find Action* найти **Data Sources and Drivers**  
1. Выбрать тип подключения PosgresSQL
2. Настроить SSH: host 127.0.0.1, port 2222, путь до приватного ключа `<папка вашего проекта>\.vagrant\machines\default\virtualbox\private_key`
3. Подключиться к БД: host 127.0.0.1, port 5432,user/password/database - skillbox/skillbox/marketplace
> Возможны проблемы с подключением к БД с примерным сообщением "пользователь не прошёл проверку подлинности по паролю". В этом случае нужно воспользоваться [решением](https://translated.turbopages.org/proxy_u/en-ru.ru.2e0a6176-638b626b-35745e68-74722d776562/https/stackoverflow.com/questions/55038942/fatal-password-authentication-failed-for-user-postgres-postgresql-11-with-pg)
## Запуск проекта в docker-compose
> Запуск проекта производится с хостовой операционной системы в режиме "Продакшн" 

В файле .env расположены "секреты" для доступа к базе данных. В переменной *POSTGRES_PORT* указывает порт проброса из контейнера в хостовую операционную систему.
Запуск осуществляется через nginx и gunicorn. Приложение должно быть доступно на порту 8181.  
**Сборка проекта**
```commandline
docker-compose build
```
**Запуск проекта**
```commandline
docker-compose up -d
```
## Участники проекта
Участник | Часовой пояс
---- | -----
Сергей Ф. | МСК
Сергей М. | МСК 
Стас | МСК
Игорь | МСК
Руслан | МСК 



# Интернет-магазин цифровых товаров






### Установка <a name="subparagraph1"></a>
Представленная ниже последовательность команд по установке проекта на компьютер, была протестирована на Windows 10 с установленным на ней python 3.7.3.
Из командной строки клонируйте проект в удобную для вас папку

```
git clone https://github.com/russe19/django-market.git
```

Создайте виртуальное окружение

```
python -m venv venv
```

Активируйте окружение и установите все необходимые библиотеки

```
pip install -r requirements.txt
```


### Запуск <a name="subparagraph2"></a>

Для запуска проекта необходимо выполнить несколько действий. 
Для сохраниения данных в моделях необходимо сделать миграции.
```
python manage.py makemigrations
```
и применить их.
```
python manage.py migrate
```
Требуется поочередно выполнить команды по установке всех хранимых в проекте файлов фикстур:
```
python manage.py loaddata users/fixtures/user.json
python manage.py loaddata users/fixtures/profile.json
python manage.py loaddata users/fixtures/profile_image.json
```
```
python manage.py loaddata catalog/fixtures/style.json
python manage.py loaddata catalog/fixtures/genre.json
python manage.py loaddata catalog/fixtures/type_offer.json
python manage.py loaddata catalog/fixtures/offer.json
python manage.py loaddata catalog/fixtures/cover.json
python manage.py loaddata catalog/fixtures/music.json
python manage.py loaddata catalog/fixtures/music_text.json
```
Активировать русскую локализацию
```
python manage.py compilemessages
```
Для запуска приложения выполним команду:
```
python manage.py runserver
```
Для начала работы следует перейти по адресу:
```
http://localhost:8000/users/register
```
и пройти процедуру регистрации.

Либо перейти по адресу:
```
http://localhost:8000/users/login
```
И пройти процедуру аутентификации
```
login: test_1
password: testinguser
```
## Обзор <a name="paragraph2"></a>
### Основная информация <a name="subparagraph3"></a>
В проекте реализовано 2 приложения: ```catalog``` и ```users```.
В приложении ```users``` хранится вся основная информация. реализована 
модель пользователя со всеми дополнительными данными о нем.
В нем реализованы такие действия как аутенификация, создание и редактирование профиля, 
просмотр и очистка корзины товаров, 
покупка товаров из корзины, просмотр истории покупок пользователя за определенный период, 
а так же просмотр API пользователей.
В приложении ```catalog``` реализован функционал по просмотру имеющихся на сайте товаров, 
просмотр детальной страницы товара и добавление нового товара на сайт.
![img.png](img.png)
На данном скриншоте продемонстрирована страница пользователя. 
Каждая страница имеет ```header``` и ```footer```, 
на некоторых страницах так же имеются баннеры.
### Тесты <a name="subparagraph4"></a>
Практически для всех моделей, форм и представлений проведено модульное тестирование.
### API <a name="subparagraph5"></a>
С помощью Django rest framework были реализованы страницы с API пользователей и товаров
![img_1.png](img_1.png) ![img_2.png](img_2.png)
Также, при передаче дополнительных данных в get-запрос, можно проводить фильтрацию.
### Транзакции <a name="subparagraph6"></a>
Покупка товаров на сайте использует механизм транцакций.
### Локализация и интернационализация <a name="subparagraph7"></a>
В проекте было так же реализован механизм локализации, Основным языком является 
английский, и в качестве дополнительного языка выбран русский. 
Форма для смены языка располагается в ```footer``` сайта.
![img_3.png](img_3.png)![img_4.png](img_4.png)
### Логирование <a name="subparagraph8"></a>
В проекте реализован механизм логирования с помощью библиотеки 
```logging```, в файле ```degug.log``` сохраняется вся необходимая информация об 
авторизации пользователей. В файле ```degug_balance.log``` сохраняется информация о 
добавлении товаров в корзину пользователя, очистке корзины пользователя и покупке товаров.
### Фикстуры и база данных <a name="subparagraph9"></a>
Все тестовые данные для базы данных хранятся в папке ```fixtures``` соответствующих 
приложений. В проекте используется база данных ```SQLite```.
### Front-end <a name="subparagraph10"></a>
Интерфейс и функции на клиентской стороне веб-сайта были реализованы на основе 
скачанной бесплатной верстки. Были внесены некоторые изменения в CSS и JS файлы.
