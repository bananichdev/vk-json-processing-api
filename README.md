# vk-json-processing-api
## Использование (Должна быть поднята Kafka и PostgreSQL)
1. Установить зависимости:
```shell
poetry install
```
2. Задать параметры приложения в app.yaml
3. Задать JSON схему в schema.json
4. Создать БД с удобным для вас названием
5. Создать .env файл вида:
```text
DB_USER=YOUR_DB_USER
DB_PASS=YOUR_DB_PASSWORD
DB_URL=localhost:5432
DB_NAME=YOUR_DB_NAME
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```
6. Создать таблицы:
```shell
poetry run alembic upgrade head
```
или создать новую миграцию:
```shell
./migrations/migrate.bash
```
7. Сгенерировать код:
```shell
./generate.bash
```
8. Запустить приложение:
```shell
poetry run python main.py
```

# K8S
Предложенные файлы для запуска сервиса находятся в папке k8s

В ближайшем будущем планируется добавить docker compose для автосборки сервиса
