import serial
import matplotlib.pyplot as plt
from collections import deque
import time

# Параметры
PORT_NAME = 'COM6'  # замените на номер своего порта, например, 'COM7'
BAUD_RATE = 115200  # скорость передачи, должна совпадать с настройкой Arduino
DATA_BUFFER_SIZE = 100  # размер буфера для хранения точек данных


def main():
    ser = serial.Serial(PORT_NAME, BAUD_RATE, timeout=1)

    data_buffer = deque(maxlen=DATA_BUFFER_SIZE)
    # plt.ion()
    # fig, ax = plt.subplots()
    # line, = ax.plot([], [], '-')
    # ax.set_title('Напряжение в реальном времени')
    # ax.set_xlabel('Время')
    # ax.set_ylabel('Напряжение (В)')
    # plt.grid(True)
    LOG_FILE_NAME = "data_log.txt"

    # Открытие файла в режиме добавления ('a')
    log_file = open(LOG_FILE_NAME, 'a')
    log_file.write("Time,Value\n")  # Заголовок CSV

    start_time = time.time()

    while True:
        try:
            raw_data = (ser.readline().decode().strip())
            #print(raw_data)
            current_time = time.time() - start_time
            log_line = f"{current_time:.3f},{raw_data}\n"
            # log_line = f"{raw_data}\n"
            # Запись в файл и сброс буфера
            log_file.write(log_line)
            log_file.flush()  # Важно для немедленной записи
            print(raw_data)
            # if raw_data:
            # voltage_value = float(raw_data) #*3.3/1023, 5)
            # current_time = time.time()
            #
            #
            #
            # data_buffer.append((current_time, voltage_value))
            #
            # x_values = [x for x, _ in data_buffer]
            # y_values = [y for _, y in data_buffer]
            #
            # line.set_data(x_values, y_values)
            # ax.relim()
            # ax.autoscale_view()
            # plt.draw()
            # plt.pause(0.01)

        except KeyboardInterrupt:
            print("Прервано")
            break


if __name__ == "__main__":
    main()