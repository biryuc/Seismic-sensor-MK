import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def plot_from_log(file_path='data_log.txt'):
    try:
        # Чтение данных из файла
        df = pd.read_csv(file_path, delimiter=',')

        # Проверка наличия нужных колонок
        if 'Time' not in df.columns or 'Value' not in df.columns:
            raise ValueError("Файл должен содержать колонки 'Time' и 'Value'")

        # Построение графика
        plt.figure(figsize=(12, 6))
        plt.plot(df['Time'], df['Value'], 'b-', linewidth=1)

        # Настройка внешнего вида
        plt.title('График напряжения из файла данных')
        plt.xlabel('Время (секунды)')
        plt.ylabel('Напряжение (В)')
        plt.grid(True)

        # Добавление временной метки
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        plt.figtext(0.95, 0.02, f"Сгенерировано: {current_time}",
                    ha="right", fontsize=8, alpha=0.7)

        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден!")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    plot_from_log()