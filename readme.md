# Investor
### Запуск:
1. Cоздание виртуального окружения `make requirements`
2. Активация виртуального окружения `source ~/bin/activate`
3. Запуск сервиса `uvicorn src.main:app`

### API:
1. Получение отчета: `POST /api/v1/reports` (json файл для теста .temp/test_data.json)

### Запрос
`curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/reports' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '@temp/test_data.json'`

### Тесты
Запуск тестов `pytest`