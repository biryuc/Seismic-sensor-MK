import pandas as pd
import matplotlib.pyplot as plt
import argparse
from datetime import datetime
import os


def load_data(file_path):
    """Загрузка данных из CSV файла"""
    try:
        # Проверяем существование файла
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден")
            return None

        # Проверяем размер файла
        if os.path.getsize(file_path) == 0:
            print(f"Файл {file_path} пуст")
            return None

        # Читаем файл - предполагаем формат: timestamp,value
        df = pd.read_csv(file_path, header=None, names=['timestamp', 'value'])

        # Преобразуем timestamp в datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        return df
    except Exception as e:
        print(f"Ошибка при загрузке файла {file_path}: {str(e)}")
        return None


def create_plots(serial_df, wifi_df):
    """Создание графиков"""
    plt.close('all')  # Закрываем все предыдущие графики

    # 1. График Serial данных
    plt.figure(1, figsize=(12, 6))
    plt.plot(serial_df['timestamp'], serial_df['value'], 'b-', label='Serial')
    plt.title('Данные с последовательного порта')
    plt.xlabel('Время')
    plt.ylabel('Значение АЦП')
    plt.grid(True)
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.tight_layout()

    # 2. График WiFi данных
    plt.figure(2, figsize=(12, 6))
    plt.plot(wifi_df['timestamp'], wifi_df['value'], 'r-', label='WiFi')
    plt.title('Данные с WiFi')
    plt.xlabel('Время')
    plt.ylabel('Значение АЦП')
    plt.grid(True)
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.tight_layout()

    # 3. Комбинированный график
    plt.figure(3, figsize=(12, 6))
    plt.plot(serial_df['timestamp'], serial_df['value'], 'b-', label='Serial')
    plt.plot(wifi_df['timestamp'], wifi_df['value'], 'r-', label='WiFi')
    plt.title('Сравнение данных Serial и WiFi')
    plt.xlabel('Время')
    plt.ylabel('Значение АЦП')
    plt.grid(True)
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.tight_layout()

    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Визуализация данных АЦП')
    parser.add_argument('--serial', action='store_true', help='Показать только данные с последовательного порта')
    parser.add_argument('--wifi', action='store_true', help='Показать только данные с WiFi')
    args = parser.parse_args()

    # Загрузка данных
    serial_df = load_data('serial_data.csv')
    wifi_df = load_data('wifi_data.csv')

    if args.serial:
        if serial_df is not None:
            plt.figure(figsize=(12, 6))
            plt.plot(serial_df['timestamp'], serial_df['value'], 'b-')
            plt.title('Данные с последовательного порта')
            plt.xlabel('Время')
            plt.ylabel('Значение АЦП')
            plt.grid(True)
            plt.gcf().autofmt_xdate()
            plt.tight_layout()
            plt.show()
        else:
            print("Не удалось загрузить Serial данные")
    elif args.wifi:
        if wifi_df is not None:
            plt.figure(figsize=(12, 6))
            plt.plot(wifi_df['timestamp'], wifi_df['value'], 'r-')
            plt.title('Данные с WiFi')
            plt.xlabel('Время')
            plt.ylabel('Значение АЦП')
            plt.grid(True)
            plt.gcf().autofmt_xdate()
            plt.tight_layout()
            plt.show()
        else:
            print("Не удалось загрузить WiFi данные")
    else:
       if serial_df is not None and wifi_df is not None:
            create_plots(serial_df, wifi_df)
       else:
            print("Не удалось загрузить один или оба файла данных")


if __name__ == "__main__":
    main()