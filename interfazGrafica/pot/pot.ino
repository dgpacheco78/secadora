#include <LiquidCrystal_I2C.h>
#include <Wire.h>

float lectura;
float voltaje;

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  lcd.init(); 
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Ruso");  
  Serial.begin(9600);
  pinMode(A0,INPUT);
}

void loop() {
  Serial.println("8");
  delay(1000);
  
  if(Serial.available()){
    lcd.print(Serial.readString());
    delay(1000);
    lcd.clear();
  }
  
}
