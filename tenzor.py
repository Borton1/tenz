import requests
from datetime import datetime, timedelta
url = "https://yandex.com/time/sync.json?geo=213"
num_requests = 5  # Количество запросов
time_differences = []

try:
    time_before_request = datetime.now()

    # Делаем GET-запрос
    response = requests.get(url)

    # Проверяем, успешен ли запрос
    response.raise_for_status()

    # Выводим "сырой" ответ
    print(response.text)

    data = response.json()

    # Получаем время и смещение
    unix_time_ms = data["time"]  # Время в мс
    offset_ms = data["clocks"]["213"]["offset"]  # Смещение для Москвы (UTC+3)

    # Переводим Unix-время в нормальное (UTC)
    unix_time_sec = unix_time_ms / 1000
    utc_time = datetime.utcfromtimestamp(unix_time_sec)

    # Преобразуем смещение из мс в часы (10800000 мс = +3 часа)
    offset_hours = offset_ms / (1000 * 60 * 60)  # 3 часа для Москвы
    moscow_time = utc_time + timedelta(hours=offset_hours)

    # Форматируем в "человеческий" вид
    human_time = moscow_time.strftime("%d.%m.%Y %H:%M:%S (МСК, UTC+3)")

    print("Текущее время в Москве:", human_time)

    unix_time_ms = data["time"]  # Unix-время в мс
    offset_ms = data["clocks"]["213"]["offset"]  # Смещение для Москвы (UTC+3)

    # Переводим Unix-время в datetime (UTC)
    unix_time_sec = unix_time_ms / 1000
    utc_time = datetime.utcfromtimestamp(unix_time_sec)

    # Добавляем смещение (UTC+3)
    moscow_time_from_api = utc_time + timedelta(hours=offset_ms / (1000 * 60 * 60))

    # Вычисляем разницу
    time_difference = moscow_time_from_api - time_before_request

    #  результаты
    print(f"Время до запроса (локальное): {time_before_request.strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"Время из API (Москва, UTC+3): {moscow_time_from_api.strftime('%d.%m.%Y %H:%M:%S')}")
    print(f"Разница: {time_difference.total_seconds():.3f} секунд")


except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе: {e}")

# замеры
for i in range(num_requests):
    try:
        # Фиксируем время ДО запроса
        time_before_request = datetime.now()

        # запрос
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Получаем время из API
        unix_time_ms = data["time"]
        offset_ms = data["clocks"]["213"]["offset"]  # 10800000 мс = +3 часа

        # Преобразуем Unix-время в datetime (UTC) и добавляем смещение
        utc_time = datetime.utcfromtimestamp(unix_time_ms / 1000)
        moscow_time = utc_time + timedelta(hours=offset_ms / (1000 * 60 * 60))

        # Вычисляем разницу (API время - локальное время)
        time_diff = (moscow_time - time_before_request).total_seconds()
        time_differences.append(time_diff)

        # Выводим результат текущего запроса
        print(f"Запрос {i + 1}: разница = {time_diff:.3f} сек")

    except requests.exceptions.RequestException as e:
        print(f"Ошибка в запросе {i + 1}: {e}")
    except Exception as e:
        print(f"Ошибка обработки {i + 1}: {e}")

# Вычисляем среднюю разницу
if time_differences:
    average_diff = sum(time_differences) / len(time_differences)
    print(f"\nСредняя разница за {num_requests} запросов: {average_diff:.3f} сек")
else:
    print("Нет данных.")