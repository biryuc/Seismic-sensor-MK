#include <ESP8266WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

const int ADC_PIN = A0;       // Пин АЦП (A0 на ESP8266)
const int SAMPLE_COUNT = 50; // Количество samples перед выводом
int adcValues[SAMPLE_COUNT];  // Буфер для хранения значений

const char* ssid = "RT-GPON-7F20";
const char* password = "92n6ZUReR4";
WiFiServer server(80);

// NTP-клиент
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 10800); // GMT+3 (10800 сек)
unsigned long currentTime = 0;  //для записи времени NTP


//Статично прописываем IP адрес МК
IPAddress local_IP(192, 168, 0, 50);
IPAddress gateway(192, 168, 0, 1);
IPAddress subnet(255, 255, 255, 0);


void setup() {
  Serial.begin(115200);       // Высокая скорость для минимизации задержек

  // Подключение к WiFi
  WiFi.config(local_IP, gateway, subnet);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.print("Подключено! IP адрес ESP8266: ");
  Serial.println(WiFi.localIP());
  

  // Инициализация NTP
  timeClient.begin();
  timeClient.update();
  
  Serial.println("Время синхронизировано с NTP");
  Serial.println(timeClient.getFormattedTime());


  server.begin();
}

void loop() {

  WiFiClient client = server.available();
  
  if (client) {
    Serial.println("Новый клиент подключен");
    
    while (client.connected()) {

      // Получаем текущее время (с шагом в секунду)
      currentTime = timeClient.getEpochTime(); 

      // 1. Заполняем буфер значениями АЦП
      for (int i = 0; i < SAMPLE_COUNT; i++) {
        adcValues[i] = analogRead(ADC_PIN);
        
      }

      // 2. Выводим все значения с корректными временными метками
      for (int i = 0; i < SAMPLE_COUNT; i++) {

        client.println(adcValues[i]);
        //delay(5);
        client.println(currentTime); // Отправляем время, прошедшее с первого сэмпла
        
      }
    }

    client.stop();
    Serial.println("Клиент отключен");
  }
}
