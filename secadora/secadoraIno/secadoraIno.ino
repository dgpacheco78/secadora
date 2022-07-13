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


void setup() {                //inicialización de objetos y variables
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Secadora");
  lcd.setCursor(0, 1);
  lcd.print("Iniciando...");
  balanza.begin(DOUT, CLK);
  delay(500);
  balanza.set_scale(-180);    //inicialización y calibración del sensor de carga
  balanza.tare(5000);         //estableciendo tare, para nuestro caso 5000 (5 Kg)
  Serial.begin(115200);       //estableciendo puerto para envio y recepción de datos
}

void loop() {
  lcd.setCursor(0, 1);                                    //mensaje de estado "listo" del sistema
  lcd.print("Sistema Listo");
  Serial.println("{\"temp\":0, \"carg\":0, \"rpm\":0}");  //envio de mensaje a python, indicando la disponibilidad
  delay(1000);                                            //del sistema
  
  if(Serial.available() > 0) {          //recepción de datos de la aplicación de python
    datoPython = Serial.readString();   //lectura del puerto
    datoPython.trim();                  //elimina espacion es blanco y saltos de linea al inicio y final de la cadena
    lcd.setCursor(0, 0);
    lcd.print(datoPython);
    Serial.println(datoPython);
    if(datoPython.equals("p")){         //si el dato de entrada es "p" inicia el proceso de precalentado del horno
      estado = 1;
    }
    if(datoPython.equals("i")){         ////si el dato de entrada es "i" inicia el proceso de secado de alimentos
      estado = 2;
    }
    delay(500);
  }
  
  while(estado == 1) {
    tempProm = (thermo1.readCelsius() + thermo2.readCelsius()) / 2;     //estado 1
    lcd.clear();                                                        //envia mensaje al lcd "precalentado"
    lcd.setCursor(0, 0);                                                //envia a la aplicacion en python, 
    lcd.print("Precalentando");                                         //temperatura y revoluciones por minuto del
    lcd.setCursor(0, 1);                                                //motor que introduce el aire al horno de secado
    lcd.print(String(tempProm));
    //{"temp":60, "tiem":120, "acti":0}
    //Serial.println("{\"temp\":" + String(tempProm) +", \"carg\":" + String(carga) + "}");
    Serial.println("{\"temp\":" + String(tempProm) +", \"carg\":0, \"rpm\":" + String(rpm) + "}");
    delay(500);
    if(Serial.available() > 0) {
      datoPython = Serial.readString();         //lee el dato del puerto serial proveniente de python
      datoPython.trim();
      if(datoPython.equals("e")){               //"e" significa paro de emergencia, en caso de que se
        estado = 0;                             //se necesite que el sistema se detenga
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Paro de emergencia");
        break;
      }
      if(datoPython.equals("i")){               //"i" indica que la temperatura ha llegado a la indicada
        estado = 2;                             //establece el estado "2"
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Enviando datos");
        break;
      }
    }
  }

  while(estado == 2) {
    tempProm = (thermo1.readCelsius() + thermo2.readCelsius()) / 2;   //estado "2"
    carga = balanza.get_units(20);                                    //lee los sensores de temperatura, carga y efecto hall (lectura)
    lcd.clear();                                                      //de revoluciones por minuto del motor de CA
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
