# Hammer-Systems-TestTask
# Как запустить
клонируйте репозиторий и создаете вертуальное окружение
```
python -m venv venv
```
включите вертуальное окружение
```
source venv/bin/activate # mac 
source venv/Scripts\\activate # windows
```
Установите зависимости
```
pip install -r requirements.txt
```
Перейдите в директепию с manage.py 
```
cd hammer
```
Выполните миграции
```
python manage.py makemigrations
python manage.py migrate
```
запустите сервер
```
python manage.py runserver
```
код будет выводится в терминале