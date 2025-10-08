import socket
import time

HOST_ESP8266 = "192.168.0.17"
HOST_ESP32 = "192.168.0.14"  # Замените на IP-адрес ESP32
HOST = HOST_ESP8266
PORT = 80


def receive_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")

        with open("data_from_wifi_log.txt", "a") as f:
            try:
                while True:
                    data = s.recv(1024)
                    if not data:
                        break
                    decoded_data = data.decode("utf-8").strip()
                    print(decoded_data)
                    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {decoded_data}\n")
                    f.flush()  # Сброс буфера записи
            except KeyboardInterrupt:
                print("Stopping data logging...")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    receive_data()