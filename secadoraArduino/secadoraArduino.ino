#include <max6675.h>
#include <LiquidCrystal_I2C.h>
#include "HX711.h"

//Declaracion de objetos y variables globales
LiquidCrystal_I2C lcd(0x27, 16, 2);
MAX6675 thermo1(5, 6, 7);
MAX6675 thermo2(8, 9, 10);
HX711 balanza;
float carga, temp2, tempProm;
const int DOUT=A1;
const int CLK=A0;


void setup() {
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Secadora");
  balanza.begin(DOUT, CLK);
  delay(500);
  balanza.set_scale(-180); 
  balanza.tare(5000);
  Serial.begin(115200);
}

void loop() {
  tempProm = (thermo1.readCelsius() + thermo2.readCelsius()) / 2;
  carga = balanza.get_units(20);
  lcd.setCursor(0, 1);
  lcd.print(String(tempProm) + ":" + String(carga));
  //{"temp":60, "tiem":120, "acti":0}
  Serial.println("{\"temp\":" + String(tempProm) +", \"carg\":" + String(carga) +"}");
  //Serial.println(String(tempProm) + ":" + String(carga));
  delay(500);
}
