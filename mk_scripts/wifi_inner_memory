#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <FS.h>
//Добавляем часы
#include <Wire.h>
#include <RTClib.h>

//объект часов
RTC_DS3231 rtc;

// === Настройки WiFi ===
const char* ssid = "RT-GPON-7F20";
const char* password = "92n6ZUReR4";

File file;

// === Настройки сети ===
IPAddress local_IP(192, 168, 0, 50);
IPAddress gateway(192, 168, 0, 1);
IPAddress subnet(255, 255, 255, 0);

// === TCP сервер ===
WiFiServer server(80);

// === NTP ===
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 10800); // GMT+3
unsigned long currentTime = 0;

// === Настройки АЦП ===
const int ADC_PIN = A0;
const int SAMPLE_COUNT = 2000;     // Кол-во измерений
const int SAMPLE_DELAY_MS = 10;   // Интервал между измерениями (мс)
const char* DATA_FILE = "/data.txt";
int adcValues[SAMPLE_COUNT]; 
int count = 0;
int value;
 

void setup() {
  Serial.begin(115200);
  Serial.println("\n=== ESP8266 ADC WiFi Stream ===");

  // Файловая система
  if (!SPIFFS.begin()) {
    Serial.println("Ошибка монтирования SPIFFS!");
    return;
  }

  // Подключение WiFi
  WiFi.config(local_IP, gateway, subnet);
  WiFi.begin(ssid, password);
  Serial.print("Подключение к WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi подключен!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  // Инициализация NTP
  timeClient.begin();
  timeClient.update();
  Serial.print("NTP время: ");
  Serial.println(timeClient.getFormattedTime());

  // Запуск TCP сервера
  server.begin();
  Serial.println("TCP сервер запущен (порт 80)");

}

// Запись данных в SPIFFS
void recordADC() {

  file = SPIFFS.open(DATA_FILE, "w");
  // if (!file) {
  //     Serial.println("Ошибка открытия файла для записи!");
  //     return;
  // }
  
  

  for (int i = 0; i < SAMPLE_COUNT; i++) {
    
    adcValues[i] = analogRead(ADC_PIN);
   
  }

  for (int i = 0; i < SAMPLE_COUNT; i++) {
   
    currentTime = timeClient.getEpochTime(); 
    file.printf("%lu,%d\n", currentTime, adcValues[i]);
   
  }
   file.close();
}

// Передача данных подключённому клиенту
void sendData(WiFiClient& client) {
  File file = SPIFFS.open(DATA_FILE, "r");
  // if (!file) {
  //   Serial.println("Файл не найден!");
  //   return;
  // }

  while (file.available()) {
    String line = file.readStringUntil('\n');
    //line.trim();
    if (line.length() > 0) {
      // формат CSV: timestamp,value
      int commaIndex = line.indexOf(',');
      if (commaIndex > 0) {
        String ts = line.substring(0, commaIndex);
        String val = line.substring(commaIndex + 1);
        client.println(val);  // сначала значение
        client.println(ts);   // потом временная метка
      }
    }

  
  }
  count++;
  file.close();
  Serial.println("Данные отправлены клиенту.");

  SPIFFS.remove(DATA_FILE);
  Serial.println("Память очищена");
}

void loop() {
  WiFiClient client = server.available();


  if (client) {
    Serial.println("Клиент подключен!");
    // String command = "";
    // int active = -1;
     while (client.connected()) {
          
          // command = client.readStringUntil('\n');
          
          // Serial.println(command);

          //if (active = 1){
              
              recordADC();
          //}
         // else if (active = 0){
              sendData(client);
             
          //}
           
     }

    
    Serial.println("Отправлено "+ String(count) + " samples"); 
    
    client.stop();
    Serial.println("Клиент отключён.");
  }
}
