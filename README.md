# Проект QuoteWeb
Данный проект подразумевает сайт со следующим функционалом:
- Авторизация/регистрация
- Показ рандомной цитаты с количеством просмотров
- Показ топ-10 цитат по лайкам
- Поставить лайк/дизлайк
- Добавить цитату.
# Технологический стек
- Backend: Django 5.0, Python 3.10+
- Database: PostgreSQL с сложными запросами
- Authentication: Сессии Django + bcrypt хеширование
- Frontend: HTML5, CSS3, Django Templates
- Security: CSRF protection, SQL injection protection
# Запуск
Сайт доступен по адресу http://90.156.211.233:8000/

# Схема БД
<img width="1033" height="510" alt="image" src="https://github.com/user-attachments/assets/a6ce5522-cbd6-4fc6-bc34-abe91f2f09e2" />

# Стурктура проекта
```
random-quote-generator/
├── main/
│   ├── models.py          # Модели: Quote, User, Like
│   ├── views.py           # Логика представлений
│   ├── urls.py            # Маршруты приложения
│   ├── templates/         # HTML шаблоны
│   └── static/           # CSS стили
├── managers/
│   └── dataBase.py       # Кастомный менеджер БД
├── requirements.txt      # Зависимости Python
└── README.md            # Документация
```

# Атвор
Батаргин Егор
Telegram: @egorbatar
