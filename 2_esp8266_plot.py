# data_visualizer.py
import matplotlib.pyplot as plt
import csv
# ESP1_FILE = "esp1_data.csv"
# ESP2_FILE = "esp2_data.csv"

ESP1_FILE = "esp1_copy.csv"
ESP2_FILE = "esp2_copy.csv"
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

def read_data(filename):
    """Читает данные из файла, возвращает списки x и y"""
    x_values = []
    y_values = []
    try:
        with open(filename, 'r') as f:
            next(f)  # Пропускаем заголовок
            for line in f:
                if line.strip():  # Пропускаем пустые строки
                    x, y = line.strip().split(',')
                    x_values.append(int(x))
                    y_values.append(int(y))
    except Exception as e:
        print(f"Ошибка чтения файла {filename}: {e}")
    return x_values, y_values


def plot_data():
    """Строит графики данных"""
    plt.figure(figsize=(14, 8))

    # Данные ESP1
    x1, y1 = read_data(ESP1_FILE)

    if x1 and y1:
        plt.plot(x1, y1, label='ESP1', color='blue', linewidth=1)

    # Данные ESP2
    x2, y2 = read_data(ESP2_FILE)
    if x2 and y2:
        plt.plot(x2, y2, label='ESP2', color='red', linewidth=1)

    # Настройки графика
    plt.title('Данные с ESP')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)

    # Форматирование осей для целых чисел
    ax = plt.gca()
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}"))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y)}"))

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_data()
    # #x1, y1 = read_data(ESP1_FILE)
    # x1, y1  = read_csv_data(ESP1_FILE)
    # # for i in range(len(y1)):
    # #     if y1[i] > 300:
    # #         print(y1[i],i)
    # plt.plot(y1)  # , label='ESP1', color='blue', linewidth=1)
    # plt.show()