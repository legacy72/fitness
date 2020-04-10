### Установка

Создать виртуальное окружение
```bash
python -m venv .env
```
Активировать виртуальное окружение
```bash
source .env/bin/activate # linux
source .env/Scripts/activate # windows
```
Установить зависимости
```bash
pip install -r requirements.txt
```
Накатить миграции
```bash
python manage.py migrate
```

### Запуск

```bash
python manage.py runserver
```

### PS

Файлик с локальными настройками можно спросить у меня
