import socket
import threading
import time

# Конфигурация устройств
DEVICES = {
    "ESP8266": {
        "ip": "192.168.0.17",
        "port": 80,
        "file": "esp8266_data.txt"
    },
    "ESP32": {
        "ip": "192.168.0.14",
        "port": 80,
        "file": "esp32_data.txt"
    }
}


class DeviceReceiver(threading.Thread):
    def __init__(self, name, config):
        threading.Thread.__init__(self)
        self.name = name
        self.ip = config["ip"]
        self.port = config["port"]
        self.filename = config["file"]
        self.running = True
        self.last_timestamp = None
        self.time_offset = 0  # Смещение времени относительно сервера

    def process_data(self, data):
        if data.startswith("TIMESTAMP:"):
            # Получена метка времени от устройства
            device_time = int(data.split(":")[1])
            server_time = int(time.time() * 1000)  # Текущее время сервера в мс
            self.time_offset = server_time - device_time
            self.last_timestamp = device_time
            print(
                f"{self.name} синхронизация: устройство={device_time}, сервер={server_time}, смещение={self.time_offset}")
            return None
        else:
            # Обычные данные с временной меткой
            current_time = int(time.time() * 1000)  # Текущее время в мс
            device_time = current_time - self.time_offset if self.last_timestamp else current_time
            return f"{device_time},{data.strip()}"

    def run(self):
        print(f"Запущен сбор данных для {self.name}")

        while self.running:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(5)
                    s.connect((self.ip, self.port))

                    with open(self.filename, "a") as f:
                        buffer = ""
                        while self.running:
                            try:
                                data = s.recv(4096).decode("utf-8")
                                if not data:
                                    break

                                buffer += data
                                lines = buffer.split("\n")

                                # Обрабатываем все завершенные строки
                                for line in lines[:-1]:
                                    processed = self.process_data(line)
                                    if processed:
                                        f.write(processed + "\n")
                                        f.flush()

                                # Оставляем неполную строку в буфере
                                buffer = lines[-1]

                            except Exception as e:
                                print(f"{self.name} ошибка: {str(e)}")
                                break

            except Exception as e:
                print(f"{self.name} ошибка подключения: {str(e)}")
                time.sleep(2)

    def stop(self):
        self.running = False

if __name__ == "__main__":
    # Создаем и запускаем потоки для каждого устройства
    receivers = [DeviceReceiver(name, config) for name, config in DEVICES.items()]

    for receiver in receivers:
        receiver.start()
        time.sleep(1)  # Задержка между запуском потоков

    try:
        # Бесконечный цикл, пока работают потоки
        while any(r.running for r in receivers):
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nОстановка потоков...")
        for receiver in receivers:
            receiver.stop()
            receiver.join()

    print("Программа завершена")