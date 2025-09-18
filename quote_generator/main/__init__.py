import sys
from pathlib import Path

# Получаем путь к корневой директории проекта (где лежит manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Добавляем этот путь в sys.path, если его там еще нет
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))