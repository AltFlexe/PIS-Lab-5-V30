# Лабораторная работа 5 — форма статьи Django

Учебный проект об аренде торговых помещений показывает статьи и позволяет вошедшему пользователю создавать новые записи. Форма проверяет название и текст, длину названия и отсутствие повторного названия. Неавторизованному пользователю форма возвращает 404.

## Запуск

При установленном Python 3.11 из корня проекта в PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/manage.py migrate
.\.venv\Scripts\python.exe src/manage.py loaddata demo
.\.venv\Scripts\python.exe src/manage.py createsuperuser
.\.venv\Scripts\python.exe src/manage.py test articles
.\.venv\Scripts\python.exe src/manage.py runserver
```

Откройте `/admin/` и войдите под созданным администратором. Затем форма доступна по адресу `/article/new/`, архив — на главной странице. Учебный набор содержит помещения и договор, но не содержит учётных записей. Ключ Django берётся из переменной `DJANGO_SECRET_KEY` или создаётся случайно для локального запуска.

Форма находится в `src/articles/templates/create_post.html`, её обработка — в `src/articles/views.py`. Модели аренды и SQLite-ограничение на пересекающиеся периоды сохранены из предыдущих работ.
