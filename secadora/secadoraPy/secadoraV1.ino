#include <max6675.h>                  //librerias necesarias para el
#include <LiquidCrystal_I2C.h>        //funcionamiento del sensor de temperatura MAX6675,
#include "HX711.h"                    //display 16x2 con I2C, sensor de carga HX711 y
#include <Servo.h>                    //servomotor

//Declaracion de objetos y variables globales
LiquidCrystal_I2C lcd(0x27, 16, 2);
MAX6675 thermo1(5, 6, 7);
MAX6675 thermo2(8, 9, 10);
HX711 balanza;
float carga, temp2, tempProm;
const int DOUT=A1;
const int CLK=A0;
String datoPython = "";
int estado = 0;
int rpm = 0;


void setup() {
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Secadora");
  lcd.setCursor(0, 1);
  lcd.print("Iniciando...");
  balanza.begin(DOUT, CLK);
  delay(500);
  balanza.set_scale(-180); 
  balanza.tare(5000);
  Serial.begin(115200);
}

void loop() {
  lcd.setCursor(0, 1);
  lcd.print("Sistema Listo");
  Serial.println("{\"temp\":0, \"carg\":0, \"rpm\":0}");
  delay(1000);
  
  if(Serial.available() > 0) {
    datoPython = Serial.readString();
    datoPython.trim();
    lcd.setCursor(0, 0);
    lcd.print(datoPython);
    Serial.println(datoPython);
    if(datoPython.equals("p")){
      estado = 1;
    }
    if(datoPython.equals("i")){
      estado = 2;
    }
    delay(500);
  }
  
  while(estado == 1) {
    tempProm = (thermo1.readCelsius() + thermo2.readCelsius()) / 2;
    //carga = balanza.get_units(20);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Precalentando");
    lcd.setCursor(0, 1);
    lcd.print(String(tempProm));
    //{"temp":60, "tiem":120, "acti":0}
    //Serial.println("{\"temp\":" + String(tempProm) +", \"carg\":" + String(carga) + "}");
    Serial.println("{\"temp\":" + String(tempProm) +", \"carg\":0, \"rpm\":" + String(rpm) + "}");
    delay(500);
    if(Serial.available() > 0) {
      datoPython = Serial.readString();
      datoPython.trim();
      if(datoPython.equals("e")){
        estado = 0;
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Paro de emergencia");
        break;
      }
      if(datoPython.equals("i")){
        estado = 2;
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Enviando datos");
        break;
      }
    }
  }

  while(estado == 2) {
    tempProm = (thermo1.readCelsius() + thermo2.readCelsius()) / 2;
    carga = balanza.get_units(20);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Enviando datos");
    lcd.setCursor(0, 1);
    lcd.print(String(tempProm) + " " + (char)223 + " " + String(carga) + " grs");
    //{"temp":60, "tiem":120, "acti":0}
    Serial.println("{\"temp\":" + String(tempProm) + ", \"carg\":" + String(carga) +", \"rpm\":" + String(rpm) + "}");
    delay(500);
    if(Serial.available() > 0) {
      datoPython = Serial.readString();
      datoPython.trim();
      if(datoPython.equals("f")){
        estado = 0;
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Fin de ciclo");
        delay(2000);
        break;
      }
      if(datoPython.equals("e")){
        estado = 0;
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Paro de emergencia");
        delay(2000);
        break;
      }
    }
  }
  
}//fin loop
