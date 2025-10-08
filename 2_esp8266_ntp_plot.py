import csv

import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


ESP1_FILE = "esp1_data.csv"
ESP2_FILE = "esp2_data.csv"

# ESP1_FILE = "esp1_copy.csv"
# ESP2_FILE = "esp2_copy.csv"


def process_data(filename):
    # Чтение данных с указанием, что файл содержит заголовок
    df = pd.read_csv(filename, names=['timestamp', 'value'], header=None)

    # Группировка по секундам
    grouped = defaultdict(list)
    for ts, val in zip(df['timestamp'], df['value']):
        # Пропускаем строки, которые не могут быть преобразованы в число
        try:
            grouped[int(float(ts))].append(val)
        except (ValueError, TypeError):
            continue

    # Создание новых временных меток с микрошагом
    processed = []
    for second, values in grouped.items():
        n = len(values)
        if n == 0:
            continue
        step = 1.0 / n  # Шаг в долях секунды

        for i, val in enumerate(values):
            micro_ts = second + i * step
            processed.append((micro_ts, val))

    return pd.DataFrame(processed, columns=['timestamp', 'value'])

def compose_ts_value(ts_data,value):
    grouped = defaultdict(list)
    for ts, val in zip(ts_data, value):
        grouped[int(ts)].append(val)

    processed = []

    sec_num = len(grouped.items())
    for second, values in grouped.items():
        n = len(values)
        if n == 0:
            continue



        if sec_num != 1:
            step = 1.0 / n  # Шаг в долях секунды


        for i, val in enumerate(values):
            micro_ts = second + i * step
            processed.append((micro_ts, val))

        sec_num-=1

    return pd.DataFrame(processed, columns=['timestamp', 'value'])

def read_csv_data(filename):
    """Читает CSV файл и возвращает два массива с данными"""
    timestamps = []
    values = []

    try:
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Пропускаем заголовок

            for row in csvreader:
                if len(row) == 2:  # Проверяем, что строка содержит оба значения
                    timestamps.append(int(row[0]))  # Первая колонка - timestamp
                    values.append(int(row[1]))  # Вторая колонка - value

    except Exception as e:
        print(f"Ошибка при чтении файла {filename}: {e}")

    return timestamps, values


def plot_data(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['value'], 'b-', linewidth=1)
    plt.xlabel('Время (секунды с микрошагом)')
    plt.ylabel('Амплитуда')
    plt.title('График амплитуды с микрошагом по времени')
    plt.grid(True)

    # Форматирование оси времени
    ax = plt.gca()
    ax.xaxis.set_major_formatter(plt.FuncFormatter(
        lambda x, _: f"{int(x)}.{int((x - int(x)) * 1000):03d}"))

    plt.show()


def plot3_data(df_esp1,ts_data_esp1,df_esp2,ts_data_esp2):
    # Создаем фигуру с тремя subplot'ами
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

    # Первый график: оригинальный сигнал
    ax1.plot(df_esp1['timestamp'], df_esp1['value'], 'b-', linewidth=1)
    ax1.plot(df_esp2['timestamp'], df_esp2['value'], 'r-', linewidth=1)
    ax1.set_xlabel('Время (секунды с микрошагом)')
    ax1.set_ylabel('Амплитуда')
    ax1.set_title('График амплитуды с микрошагом по времени')
    ax1.grid(True)

    # Второй график: только timestamp
    #ax2.plot(df['timestamp'], 'r-', linewidth=1)
    ax2.plot(ts_data_esp1, 'r-', linewidth=1)
    ax2.plot(ts_data_esp2, 'g-', linewidth=1)
    ax2.set_xlabel('Индекс')
    ax2.set_ylabel('Время (секунды)')
    ax2.set_title('График временных меток (timestamp)')
    ax2.grid(True)

    # Третий график: только value
    ax3.plot(df_esp1['value']/df_esp1['value'].max(), 'g-', linewidth=1)
    ax3.plot(df_esp2['value']/df_esp2['value'].max(), 'r-', linewidth=1)
    ax3.set_xlabel('Индекс')
    ax3.set_ylabel('Амплитуда')
    ax3.set_title('График значений амплитуды')
    ax3.grid(True)

    # Форматирование оси времени для первого графика
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(
        lambda x, _: f"{int(x)}.{int((x - int(x)) * 1000):03d}"))

    # Автоматическое выравнивание subplot'ов
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":

    ts_data_esp1,value_esp1 = read_csv_data(ESP1_FILE)
    ts_data_esp2,value_esp2 = read_csv_data(ESP2_FILE)

    processed_df_esp1 = compose_ts_value(ts_data_esp1,value_esp1)
    processed_df_esp2 = compose_ts_value(ts_data_esp2,value_esp2)

    plot3_data(processed_df_esp1,ts_data_esp1,processed_df_esp2,ts_data_esp2)
