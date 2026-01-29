import os
import re
from pathlib import Path


def find_imports_in_file(file_path):
    """Находит все импорты в Python файле"""
    imports = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

            # Ищем import statements
            # 1. import module
            # 2. import module as alias
            # 3. from module import something
            patterns = [
                r'^\s*import\s+([\w\.]+)',  # import module
                r'^\s*from\s+([\w\.]+)\s+import',  # from module import
            ]

            for line in content.split('\n'):
                line = line.strip()
                for pattern in patterns:
                    match = re.match(pattern, line)
                    if match:
                        module = match.group(1).split('.')[0]  # Берем только корневой модуль
                        imports.add(module)
    except:
        pass
    return imports


def scan_project(project_path):
    """Сканирует весь проект на импорты"""
    all_imports = set()

    for root, dirs, files in os.walk(project_path):
        # Игнорируем виртуальные окружения и скрытые папки
        if 'venv' in root or '.git' in root or '__pycache__' in root:
            continue

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                imports = find_imports_in_file(file_path)
                all_imports.update(imports)

    return sorted(all_imports)


if __name__ == '__main__':
    project_dir = '.'  # Текущая директория
    imports = scan_project(project_dir)

    print("Найдены импорты:")
    print("=" * 50)
    for imp in imports:
        print(f"  - {imp}")
    print("=" * 50)

    # Сохраняем в файл
    with open('found_imports.txt', 'w', encoding='utf-8') as f:
        for imp in imports:
            f.write(f"{imp}\n")

    print(f"\nСписок сохранен в found_imports.txt")
    print("\nВНИМАНИЕ: Некоторые модули могут быть встроенными (os, sys, re и т.д.)")