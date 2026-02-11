#include <LiquidCrystal.h>
#include <DHT.h>

// ----- LCD SETUP -----
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

// ----- DHT11 SETUP -----
#define DHTPIN 3        // Your sensor is on digital pin 3
#define DHTTYPE DHT11   // Sensor type
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  lcd.begin(16, 2);   // 16 columns, 2 rows
  dht.begin();        // Start the DHT sensor

  lcd.setCursor(0, 0);
  lcd.print("Temp & Humid");
  delay(1000);
}

void loop() {
  float h = dht.readHumidity();          // Humidity %
  float f = dht.readTemperature(true);   // Fahrenheit

  // If sensor fails, show error
  if (isnan(h) || isnan(f)) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Sensor Error");
    delay(1000);
    return;
  }

  // ----- DISPLAY TEMP -----
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Temp: ");
  lcd.print(f, 1);   // 1 decimal place
  lcd.print(" F");

  // ----- DISPLAY HUMIDITY -----
  lcd.setCursor(0, 1);
  lcd.print("Hum:  ");
  lcd.print(h, 1);
  lcd.print(" %");

  delay(1000);  // Update every second
