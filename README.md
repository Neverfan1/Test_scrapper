# Microservice of Test Scrapper


## Требования к установке
```sh
1. устанавливаем poetry
2. копируем файл .env_example в .env и указываем валидные данные 
3. запускаем проект через командную строку poetry run python main.py
```

### .env example
```sh
SERVER_HOST='127.0.0.1'
SERVER_PORT=8007
DATABASE_URL="postgresql+psycopg2://login:password@host/db_name"

CORS_ALLOWED_ORIGINS='["http://localhost:8000", "http://127.0.0.1:8000"]'
```
