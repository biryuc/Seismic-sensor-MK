import socket
import threading
import time
import csv
import numpy as np
from zeroconf import Zeroconf, ServiceBrowser
import time
# Конфигурация
ESP1_IP = "192.168.0.50"
ESP2_IP = "192.168.0.51"

# ESP1_IP = socket.gethostbyname("esp1.local")
# ESP2_IP = socket.gethostbyname("esp2.local")

PORT = 80
BUFFER_SIZE = 1024
ESP1_FILE = "esp1_data.csv"
ESP2_FILE = "esp2_data.csv"
running = True

# ESP1_IP = None
# ESP2_IP = None

class MyListener:
    def add_service(self, zeroconf, type, name):
        global ESP1_IP, ESP2_IP
        info = zeroconf.get_service_info(type, name)
        if info:
            ip = info.parsed_addresses()[0]
            print(f"Найдено устройство: {name}, IP: {ip}")

            # Разделяем по имени сервиса
            if "esp1" in name.lower():
                ESP1_IP = ip
            elif "esp2" in name.lower():
                ESP2_IP = ip


def setup_csv(filename):
    """Создает CSV файл с заголовками"""
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "value"])


def receive_data(esp_ip, esp_name, filename):
    global running
    print(f"Подключение к {esp_name} ({esp_ip})...")

    buffer = ""
    expected_value = True  # Ожидаем значение (True) или временную метку (False)
    last_value = None

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((esp_ip, PORT))
            print(f"Соединение с {esp_name} установлено")

            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                while running:
                    data = s.recv(BUFFER_SIZE).decode('utf-8')
                    if not data:
                        continue

                    buffer += data

                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        line = line.strip()

                        if not line:
                            continue

                        try:
                            if expected_value:
                                # Ожидаем значение
                                last_value = int(line)
                                expected_value = False
                            else:
                                # Ожидаем временную метку
                                timestamp = np.uint64(line)
                                writer.writerow([timestamp, last_value])
                                print(f"{esp_name}: {timestamp} - {last_value}")
                                expected_value = True
                        except (ValueError, TypeError) as e:
                            print(f"Ошибка парсинга данных: {e}")
                            expected_value = True  # Сброс состояния при ошибке

    except Exception as e:
        print(f"Ошибка с {esp_name}: {e}")
    finally:
        print(f"Соединение с {esp_name} закрыто")


def main():
    # zeroconf = Zeroconf()
    # listener = MyListener()
    # browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
    #
    # # Ждем немного, чтобы устройства успели объявиться
    # print("Ожидание обнаружения ESP...")
    # time.sleep(5)
    #
    # zeroconf.close()

    print(f"ESP1_IP = {ESP1_IP}")
    print(f"ESP2_IP = {ESP2_IP}")

    setup_csv(ESP1_FILE)
    setup_csv(ESP2_FILE)

    thread1 = threading.Thread(target=receive_data, args=(ESP1_IP, "ESP1", ESP1_FILE))
    thread2 = threading.Thread(target=receive_data, args=(ESP2_IP, "ESP2", ESP2_FILE))

    thread1.start()
    thread2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        global running
        running = False
        thread1.join()
        thread2.join()
        print("Прием данных завершен")


if __name__ == "__main__":
    main()