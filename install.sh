#!/bin/bash

# Выходим, если какая-то команда завершилась ошибкой
set -e

echo "=== Установка SecureFile Pro ==="

# 1. Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "Ошибка: Python3 не установлен!"
    exit 1
fi

# 2. Создаем виртуальное окружение, если его нет
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения venv..."
    python3 -m venv venv
fi

# 3. Устанавливаем зависимости
echo "Установка зависимостей..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# 4. Делаем файлы исполняемыми
echo "Настройка прав доступа..."
chmod +x securefile

# 5. Создаем символическую ссылку в системе
echo "Интеграция в систему (потребуются права sudo)..."
sudo ln -sf "$(pwd)/securefile" /usr/local/bin/securefile

echo "=== Установка успешно завершена! ==="
echo "Теперь вы можете запустить приложение командой: securefile"
