#include <max6675.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <Ticker.h>
#include <Servo.h>

#define PIN_TRIG 2
#define PIN_ECHO 3
#define PIN_POT A2
#define PIN_LED 4
#define PIN_MOT 5

Servo mot;
MAX6675 sensorT1(5, 6, 7);  //5:SCK 6:CS 7:SO
MAX6675 sensorT2(8, 9, 10);  //8:SCK 9:CS 10:SO
LiquidCrystal_I2C lcd(0x27, 16, 2);

int value_led = 0;
int value_mot = 0;
float value_temp1 = -1.0, value_temp2 = -1.0;
float value_tempProm = 0;
float value_peso = 0;

void fnPeso(){
  float peso;
  peso =analogRead(PIN_POT);
  if (peso != value_peso){
    value_peso = peso;
    //lcd.setCursor(0,1);
    //lcd.print("Peso: " + (String)peso);    
  }  
}


void fnTemperatura(){
  float temp1, temp2, tempProm;
  temp1 = sensorT1.readCelsius();
  temp2 = sensorT2.readCelsius();
  tempProm = (temp1 + temp2) / 2;
  //if (temp1 != value_temp1 || temp2 != value_temp2){
  // value_temp1 = temp1;
  //  value_temp2 = temp2;
  if (tempProm != value_tempProm){
    value_tempProm = tempProm;
    //lcd.setCursor(0,0);
    //lcd.print((String)tempProm + "°C");
    //lcd.setCursor(0,1);
    //lcd.print("Sensor 2: " + (String)temp2);
    //lcd.print("Sensor 2: " + (String)value_temp2);
  }  
}

Ticker ticPeso(fnPeso,500);
Ticker ticTemperatura(fnTemperatura,500);

void fnActuadores(String cad){//tiempo y temperatura
  Serial.print("actuadores");
  int pos;
  String label,value;
  cad.trim();
  cad.toLowerCase();
  pos = cad.indexOf(':');
  label= cad.substring(0,pos);
  value= cad.substring(pos+1); 

  if (label.equals("tie")){//formato > HH:MM
    if(value_mot != value.toInt()){
      value_mot = value.toInt();  
      lcd.setCursor(0,1);
      lcd.print("Temp: " + (String)value_mot);
      Serial.println(value_mot);
    }    
  }
  
  if (label.equals("tem")){//formato int
    if(value_led != value.toInt()){
      value_led = value.toInt();
      mot.write(value_mot); 
      lcd.setCursor(0,1);
      lcd.print("led" + (String)value_led);
      Serial.println(value_led);
    }
  }
}

void setup() {
  Serial.begin(9600);
  delay(30);
  // config pines
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  pinMode(PIN_LED, OUTPUT);
  mot.attach(PIN_MOT);

  //Initial values
  digitalWrite(PIN_LED,value_led);
  mot.write(value_mot); 

  lcd.init();
  lcd.backlight();
  lcd.print("Secadora::UTIM");
  delay(1000);
  lcd.clear();

  ticPeso.start();
  ticTemperatura.start();
}



void loop() {
  ticPeso.update();
  ticTemperatura.update();

  value_tempProm = 0;
  value_peso = 0;
  lcd.setCursor(0,0);
  lcd.print((String)value_tempProm + "°, " + (String)value_peso);
  /*
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Temp: " + (String)ktc.readCelsius());
  delay(500);
  */
  if(Serial.available()){
    fnActuadores(Serial.readString());
  }
}
