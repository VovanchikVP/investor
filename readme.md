# Investor
### Запуск:
1. Cоздание виртуального окружения `make requirements`
2. Активация виртуального окружения `source ~/bin/activate`
3. Запуск сервиса `uvicorn src.main:app`

### API:
1. Доступ к swagger: `/docs`

### Тесты
Запуск тестов `pytest`

### Миграции на основе alembic
Автоматическое создание миграций: `alembic revision --autogenerate -m "init"`
Применение миграции: `alembic upgrade head`
Отмена миграции: `alembic downgrade -1 `