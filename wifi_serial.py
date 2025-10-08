import serial
import socket
import threading
from datetime import datetime

# Конфигурация
SERIAL_PORT = 'COM6'  # Замените на ваш COM-порт
BAUDRATE = 230400
WIFI_IP = '192.168.0.19'  # Замените на IP ESP8266 192.168.0.19
WIFI_PORT = 80

# Файлы для записи
SERIAL_LOG_FILE = 'serial_data.csv'
WIFI_LOG_FILE = 'wifi_data.csv'


class DataCollector:
    def __init__(self):
        self.running = True

    def read_serial(self):
        try:
            ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
            print(f"Подключено к последовательному порту {SERIAL_PORT}")

            while self.running:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    try:
                        value = int(line)
                        timestamp = datetime.now().isoformat()
                        with open(SERIAL_LOG_FILE, 'a') as f:
                            f.write(f"{timestamp},{value}\n")
                    except ValueError:
                        pass
        except Exception as e:
            print(f"Ошибка последовательного порта: {e}")
        finally:
            if 'ser' in locals():
                ser.close()

    def read_wifi(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((WIFI_IP, WIFI_PORT))
            print(f"Подключено к WiFi {WIFI_IP}:{WIFI_PORT}")

            while self.running:
                data = sock.recv(1024).decode('utf-8')
                if not data:
                    continue

                for line in data.splitlines():
                    line = line.strip()
                    if line:
                        try:
                            value = int(line)
                            timestamp = datetime.now().isoformat()
                            with open(WIFI_LOG_FILE, 'a') as f:
                                f.write(f"{timestamp},{value}\n")
                        except ValueError:
                            pass
        except Exception as e:
            print(f"Ошибка WiFi соединения: {e}")
        finally:
            sock.close()

    def stop(self):
        self.running = False


def main():
    collector = DataCollector()

    # Создаем файлы с заголовками, если они не существуют
    for file in [SERIAL_LOG_FILE, WIFI_LOG_FILE]:
        try:
            with open(file, 'x') as f:
                f.write("timestamp,value\n")
        except FileExistsError:
            pass

    # Запуск потоков
    serial_thread = threading.Thread(target=collector.read_serial)
    wifi_thread = threading.Thread(target=collector.read_wifi)

    serial_thread.start()
    wifi_thread.start()

    try:
        while True:
            input("Нажмите Enter для остановки...")
            break
    except KeyboardInterrupt:
        pass
    finally:
        print("Остановка...")
        collector.stop()
        serial_thread.join()
        wifi_thread.join()
        print("Сбор данных завершен.")


if __name__ == "__main__":
    main()