import matplotlib.pyplot as plt
from datetime import datetime

# 1. Чтение данных из файла
filename = "data_from_wifi_log.txt"
adc_values = []  # Массив всех значений АЦП

with open(filename, "r") as f:
    for line in f:
        if " - " in line:
            # Разделяем строку на временную метку и данные
            timestamp_str, data_str = line.strip().split(" - ")

            # Обрабатываем случаи, когда строка начинается с запятой
            if data_str.startswith(','):
                data_str = data_str[1:]  # Удаляем первую запятую

            # Разбиваем строку данных по запятым и конвертируем в числа
            values = [int(x) if x.strip().isdigit() else 0 for x in data_str.split(',')]
            adc_values.extend(values)

# 2. Построение графика
plt.figure(figsize=(14, 6))
plt.plot(adc_values, 'b-', linewidth=0.8)
plt.xlabel("Номер отсчета", fontsize=12)
plt.ylabel("Значение АЦП", fontsize=12)
plt.title("График АЦП данных из файла", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.7)

# Добавляем горизонтальную линию на нуле
plt.axhline(0, color='gray', linestyle='-', linewidth=0.5)

# Оптимизируем отображение для большого количества точек
if len(adc_values) > 1000:
    plt.margins(x=0.01)

plt.tight_layout()
plt.show()