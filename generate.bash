#!/bin/bash

export PYTHONPATH=$(pwd)

poetry run python cli/init.py
if [ $? -ne 0 ]; then
    echo "Ошибка во время выполнения init.py"
    exit 1
fi

poetry run python cli/generate_models.py
if [ $? -ne 0 ]; then
    echo "Ошибка во время выполнения generate_models.py"
    exit 1
fi

poetry run python cli/generate_rest.py
if [ $? -ne 0 ]; then
    echo "Ошибка во время выполнения generate_rest.py"
    exit 1
fi

echo "Все команды выполнены успешно"
