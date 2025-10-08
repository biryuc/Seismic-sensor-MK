import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta


def read_sensor_data(filename):
    """Чтение данных из файла с временными метками и значениями"""
    timestamps = []
    amplitudes = []

    with open(filename, 'r') as f:
        for line in f:
            if not line.strip():
                continue

            parts = line.strip().split(',')
            if len(parts) < 2:
                continue

            try:
                # Первое значение - временная метка
                timestamp = int(parts[0])
                # Остальные значения - амплитуды
                for amp in parts[1:]:
                    if amp:  # Пропускаем пустые значения
                        amplitudes.append(float(amp))
                        timestamps.append(timestamp)
            except (ValueError, IndexError) as e:
                print(f"Ошибка обработки строки: {line.strip()}, ошибка: {e}")
                continue

    return timestamps, amplitudes


# Загрузка данных
esp8266_ts, esp8266_amp = read_sensor_data("esp8266_data.txt")
esp32_ts, esp32_amp = read_sensor_data("esp32_data.txt")

# Проверка наличия данных
if not esp8266_ts or not esp32_ts:
    raise ValueError("Нет данных для отображения. Проверьте входные файлы.")

# Нормализация временных меток относительно начала записи
min_time = min(min(esp8266_ts), min(esp32_ts))
esp8266_rel_ts = [(ts - min_time) / 1000.0 for ts in esp8266_ts]  # переводим в секунды
esp32_rel_ts = [(ts - min_time) / 1000.0 for ts in esp32_ts]  # переводим в секунды

# Создание графика
plt.figure(figsize=(16, 8))

# Отрисовка данных
plt.plot(esp8266_rel_ts, esp8266_amp, 'b-', label='ESP8266', alpha=0.7, linewidth=1)
plt.plot(esp32_rel_ts, esp32_amp, 'r-', label='ESP32', alpha=0.7, linewidth=1)

# Настройка осей и оформления
plt.xlabel('Время (секунды)', fontsize=12)
plt.ylabel('Амплитуда', fontsize=12)
plt.title(f'Сравнение сигналов с ESP8266 и ESP32\nНачальное время: {datetime.fromtimestamp(min_time / 1000)}',
          fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=12)

# Оптимизация отображения
plt.tight_layout()

# Добавление дополнительной информации
plt.text(0.01, 0.95, f"Всего точек:\nESP8266: {len(esp8266_amp)}\nESP32: {len(esp32_amp)}",
         transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.8))

plt.show()