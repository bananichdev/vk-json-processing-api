#!/bin/bash

if [ -z "$DB_USER" ]; then
  echo "Ошибка: переменная окружения DB_USER не задана."
  exit 1
fi

if [ -z "$DB_PASS" ]; then
  echo "Ошибка: переменная окружения DB_PASS не задана."
  exit 1
fi

if [ -z "$DB_URL" ]; then
  echo "Ошибка: переменная окружения DB_URL не задана."
  exit 1
fi

if [ -z "$DB_NAME" ]; then
  echo "Ошибка: переменная окружения DB_NAME не задана."
  exit 1
fi

if [ -z "$1" ]; then
  echo "Ошибка: имя ревизии не задано."
  echo "Использование: $0 <revision_name>"
  exit 1
fi

REVISION_NAME=$1

poetry run alembic revision --autogenerate -m "$REVISION_NAME"
if [ $? -ne 0 ]; then
  echo "Ошибка при выполнении команды 'poetry run alembic revision --autogenerate'"
  exit 1
fi

poetry run alembic upgrade head
if [ $? -ne 0 ]; then
  echo "Ошибка при выполнении команды 'poetry run alembic upgrade head'"
  exit 1
fi

echo "Миграция прошла успешно"
