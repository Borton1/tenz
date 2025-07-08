import json
import sys
import random


def generate_versions(template):
    """Генерируем 2 случайных номера версии на основе шаблона"""
    versions = []
    for _ in range(2):
        parts = []
        for x in template.split('.'):
            if x == '*':
                parts.append(str(random.randint(0, 9)))
            else:
                parts.append(x)
        versions.append('.'.join(parts))
    return versions


def version_key(v):
    """Ключ для сортировки версий"""
    parts = v.split('.')  # Разделяем строку по точкам
    numbers = [int(p) for p in parts]  # Преобразуем каждую часть в число
    version_tuple = tuple(numbers)

    return version_tuple


def is_version_older(v1, v2):
    """Проверяем, что версия v1 старше (меньше) v2"""
    parts1 = list(map(int, v1.split('.')))
    parts2 = list(map(int, v2.split('.')))

    # Дополняем более короткую версию нулями
    max_len = max(len(parts1), len(parts2))
    parts1 += [0] * (max_len - len(parts1))
    parts2 += [0] * (max_len - len(parts2))

    return parts1 < parts2


def main(version_param, config_file):
    try:
        # Чтение конфигурационного файла
        with open(config_file, 'r') as f:
            # Удаляем лишние символы и парсим как JSON
            content = f.read().replace('“', '"').replace('”', '"')
            config = json.loads(content)

        # Генерация всех версий
        all_versions = []
        for key, template in config.items():
            # Удаляем кавычки, если они есть
            template = str(template).strip('"\'')
            generated = generate_versions(template)
            print(f"{key} ({template}): {generated}")
            all_versions.extend(generated)

        # Сортировка всех версий
        sorted_versions = sorted(all_versions, key=version_key)
        print("\nВсе версии (отсортированные):")
        for v in sorted_versions:
            print(v)

        # Фильтрация версий старше указанной
        older_versions = []
        for version in sorted_versions:
            if is_version_older(version, version_param):
                older_versions.append(version)
        print(f"\nВерсии старше {version_param}:")
        for v in older_versions:
            print(v)

    except FileNotFoundError:
        print(f"Ошибка: файл {config_file} не найден")
    except json.JSONDecodeError:
        print("Ошибка: некорректный JSON в конфигурационном файле")
    except Exception as e:
        print(f"Ошибка: {str(e)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python tenzor2.py <версия> <конфиг_файл>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])