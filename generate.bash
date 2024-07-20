#!/bin/bash

export PYTHONPATH=$(pwd)

poetry run python cli/init.py
if [ $? -ne 0 ]; then
    echo "Error: Failed to run init.py"
    exit 1
fi

poetry run python cli/generate_models.py
if [ $? -ne 0 ]; then
    echo "Error: Failed to run generate_models.py"
    exit 1
fi

poetry run python cli/generate_rest.py
if [ $? -ne 0 ]; then
    echo "Error: Failed to run generate_rest.py"
    exit 1
fi

echo "All commands executed successfully"
