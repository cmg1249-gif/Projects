#include <LiquidCrystal.h>
#include <DHT.h>

// ----- LCD SETUP -----
LiquidCrystal lcd(7, 8, 9, 10, 11, 12);

// ----- DHT11 SETUP -----
#define DHTPIN 3
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  lcd.begin(16, 2);
  dht.begin();

  lcd.setCursor(0, 0);
  lcd.print("Temp & Humid");
  delay(1000);
}

void loop() {
  float h = dht.readHumidity();
  float f = dht.readTemperature(true);

  if (isnan(h) || isnan(f)) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Sensor Error");
    delay(1000);
    return;
  }

  // ----- Calculate minutes running -----
  unsigned long ms = millis();
  unsigned long minutesRunning = ms / 60000;  // 60000 ms = 1 minute

  lcd.clear();

  // ----- LINE 1: TEMP & HUMID -----
  lcd.setCursor(0, 0);
  lcd.print("T:");
  lcd.print(f, 0);
  lcd.print("F H:");
  lcd.print(h, 0);
  lcd.print("%");

  // ----- LINE 2: MINUTES RUNNING -----
  lcd.setCursor(0, 1);
  lcd.print("Up: ");
  lcd.print(minutesRunning);
  lcd.print(" min");

  delay(1000);
}
