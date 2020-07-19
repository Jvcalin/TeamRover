//Includes
#include <Wire.h>
#include <Adafruit_INA219.h>
#include "Adafruit_seesaw.h"

//Private Variables

//Ultrasonic Sensor
//#define fEchoPin 12  //ESP8266 GPIOs
//#define rEchoPin 13
//#define lEchoPin 16
//#define bEchoPin 15

#define fEchoPin 17  //ESP32 GPIOs
#define rEchoPin 21
#define lEchoPin 16
#define bEchoPin 19

#define fTrigPin 11  //Seesaw GPIOs
#define rTrigPin 10  
#define lTrigPin 14  
#define bTrigPin 15 

#define esp32BattPin A13

#define vibrationPin A5
//#define ledPin 9
//#define opSensorPin A0 //Optical Sensor
#define SEESAW_ADDRESS2 (0x4A)

#define FRONT 1001;
#define BACK 1002;
#define LEFT 1003;
#define RIGHT 1004;


int fDistance = 99;
int bDistance = 99;
int lDistance = 99;
int rDistance = 99;

Adafruit_INA219 ina219(0x41);
//Adafruit_INA219 ina219_A;
//Adafruit_INA219 ina219_B(0x41);

//long duration, inches, cm;


Adafruit_seesaw ss1;
//Adafruit_seesaw ss2;

void SetupSensors() {
    //SPrint("Starting");
    //SPrintln("Start Program");

    if(!ss1.begin()){
      SPrintln("ERROR!");
      //while(1);
    }
      else SPrintln("seesaw1 started");
      
    //if(!ss2.begin(SEESAW_ADDRESS2,-1,true)){
    //  SPrintln("ERROR!");
    //  //while(1);
    //}
    //  else SPrintln("seesaw2 started");  

        
    //pinMode(opSensorPin, INPUT);
    ss1.pinMode(fTrigPin, OUTPUT);
    pinMode(fEchoPin, INPUT);
    ss1.pinMode(bTrigPin, OUTPUT);
    pinMode(bEchoPin, INPUT);
    ss1.pinMode(lTrigPin, OUTPUT);
    pinMode(lEchoPin, INPUT);
    ss1.pinMode(rTrigPin, OUTPUT);
    pinMode(rEchoPin, INPUT);

    pinMode(esp32BattPin, OUTPUT);
    //ss1.pinMode(ledPin, OUTPUT);
    
    // Initialize the INA219.
    // By default the initialization will use the largest range (32V, 2A).  However
    // you can call a setCalibration function to change this range (see comments).
    ina219.begin();
    // To use a slightly lower 32V, 1A range (higher precision on amps):
    //ina219.setCalibration_32V_1A();
    // Or to use a lower 16V, 400mA range (higher precision on volts and amps):
    ina219.setCalibration_16V_400mA();

}

//Public Functions

void SensorsTick() {
  ultrasonicSensorDetectAll();
}

//bool OpSensorDetect() {
//  int reading = analogRead(opSensorPin);
//  float proximityV = (float)reading * 5.0 / 1023.0;
//  //if (digitalRead(echoPin) == HIGH) {
//  if (reading > 60) {
//    SPrintln(reading);
//    //SPrintln("op!");
//    return true;
//  }
//  else {
//    SPrintln(reading);
//    return false;
//  }
//}

void printUltrasonicSensorReadings() {
      
  SPrint("F");
  SPrint(fDistance);
  SPrint("-L");
  SPrint(lDistance);
  SPrint("-R");
  SPrint(rDistance);
  SPrint("-B");
  SPrint(bDistance);
  SPrint("-");
  SPrint(getCurrentAction());
  SPrint("-S");
  SPrint(getCurrSpeed());
  SPrintln("");

}

int getFrontDistance() {
  return fDistance;
}
int getBackDistance() {
  return bDistance;
}
int getLeftDistance() {
  return lDistance;
}
int getRightDistance() {
  return rDistance;
}

void ultrasonicSensorDetectAll() {
  ultrasonicSensorDetectLeft();
  ultrasonicSensorDetectFront();
  ultrasonicSensorDetectBack();
  ultrasonicSensorDetectRight();
}
void ultrasonicSensorDetectFront() {
   //SPrint("Front: ");
   fDistance = ultrasonicSensorDetect(fTrigPin, fEchoPin);
}
void ultrasonicSensorDetectBack() {
   //SPrint("Back: ");
   bDistance = ultrasonicSensorDetect(bTrigPin, bEchoPin);
}
void ultrasonicSensorDetectLeft() {
   //SPrint("Left: ");
   lDistance = ultrasonicSensorDetect(lTrigPin, lEchoPin);
}
void ultrasonicSensorDetectRight() {
   //SPrint("Right: ");
   rDistance = ultrasonicSensorDetect(rTrigPin, rEchoPin);
}

int ultrasonicSensorDetect(int trigPin, int echoPin) {
  long duration = 0;
  long inches = 0;
  long cm = 0;
  
  ss1.digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  ss1.digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  ss1.digitalWrite(trigPin, LOW);

  //pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH); //, 20000);

  cm = (duration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343
  inches = (duration/2) / 74;   // Divide by 74 or multiply by 0.0135

  return inches;
}


void KnockOccurred(int value) {
  SPrint("Vibration: ");
  SPrintln(value);
  PlaySwoopDown();
  if (currentAction == 0) 
    currentAction = 1;
}

void SenseVibration() {
  int value = analogRead(vibrationPin);
  if (value > 950)
    KnockOccurred(value);
}


float readBatterySensor() {
  float shuntvoltage = 0;
  float busvoltage = 0;
  float current_mA = 0;
  float loadvoltage = 0;
  float power_mW = 0;

  shuntvoltage = ina219.getShuntVoltage_mV();
  busvoltage = ina219.getBusVoltage_V();
  current_mA = ina219.getCurrent_mA();
  power_mW = ina219.getPower_mW();
  loadvoltage = busvoltage + (shuntvoltage / 1000);
  /*
  SPrint("Bus Voltage:   "); SPrint(busvoltage); SPrintln(" V");
  SPrint("Shunt Voltage: "); SPrint(shuntvoltage); SPrintln(" mV");
  SPrint("Load Voltage:  "); SPrint(loadvoltage); SPrintln(" V");
  SPrint("Current:       "); SPrint(current_mA); SPrintln(" mA");
  SPrint("Power:         "); SPrint(power_mW); SPrintln(" mW");
  SPrintln("");

  delay(2000); */

  //https://forums.adafruit.com/viewtopic.php?f=19&t=127291#:~:text=The%20bus%20voltage%20is%20the,in%20series%20with%20the%20load..
  /*
   * The bus voltage is the total voltage between power and GND. It is the sum of the load voltage and the shunt voltage.
The load voltage is the voltage going to the load.
The shunt voltage is the voltage drop across the shunt resistor that is in series with the load
   */
  return busvoltage;
}

float readESP32BatterySensor() {
  return ((float)analogRead(esp32BattPin))/1000;
}
//Private Functions
