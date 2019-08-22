//Includes
#include <Wire.h>
#include <Adafruit_INA219.h>
#include "Adafruit_seesaw.h"

//Private Variables
#define fTrigPin 12  //Ultrasonic Sensor
#define fEchoPin 14
#define bTrigPin 15  //Ultrasonic Sensor
#define bEchoPin 13
#define lTrigPin 11  //Ultrasonic Sensor
#define lEchoPin 10
#define rTrigPin 15  //Ultrasonic Sensor
#define rEchoPin 14

#define opSensorPin A0 //Optical Sensor


int FRONT = 1001;
int BACK = 1002;
int LEFT = 1003;
int RIGHT = 1004;

Adafruit_INA219 ina219(0x41);
//Adafruit_INA219 ina219_A;
//Adafruit_INA219 ina219_B(0x41);

//long duration, inches, cm;

Adafruit_seesaw ss;

void SetupSensors() {
    //SPrint("Starting");
    SPrintln("Start Program");

    if(!ss.begin()){
      SPrintln("ERROR!");
      //while(1);
    }
      else SPrintln("seesaw started");
    
    //pinMode(opSensorPin, INPUT);
    pinMode(fTrigPin, OUTPUT);
    pinMode(fEchoPin, INPUT);
    pinMode(bTrigPin, OUTPUT);
    pinMode(bEchoPin, INPUT);
    ss.pinMode(lTrigPin, OUTPUT);
    ss.pinMode(lEchoPin, INPUT);
    ss.pinMode(rTrigPin, OUTPUT);
    ss.pinMode(rEchoPin, INPUT);

    // Initialize the INA219.
    // By default the initialization will use the largest range (32V, 2A).  However
    // you can call a setCalibration function to change this range (see comments).
    ina219.begin();
    // To use a slightly lower 32V, 1A range (higher precision on amps):
    //ina219.setCalibration_32V_1A();
    // Or to use a lower 16V, 400mA range (higher precision on volts and amps):
    //ina219.setCalibration_16V_400mA();

}

//Public Functions
bool OpSensorDetect() {
  int reading = analogRead(opSensorPin);
  float proximityV = (float)reading * 5.0 / 1023.0;
  //if (digitalRead(echoPin) == HIGH) {
  if (reading > 60) {
    SPrintln(reading);
    //SPrintln("op!");
    return true;
  }
  else {
    SPrintln(reading);
    return false;
  }
}

void ultrasonicSensorDetectFront() {
      ultrasonicSensorDetect(fTrigPin, fEchoPin);
}
void ultrasonicSensorDetectBack() {
      ultrasonicSensorDetect(bTrigPin, bEchoPin);
}
void ultrasonicSensorDetectLeft() {
      ultrasonicSensorDetectSS(lTrigPin, lEchoPin);
}
void ultrasonicSensorDetectRight() {
      ultrasonicSensorDetectSS(rTrigPin, rEchoPin);
}
void ultrasonicSensorDetectSS(int trigPin, int echoPin) {
  long duration = 0;
  long inches = 0;
  long cm = 0;

  ss.digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  ss.digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  ss.digitalWrite(trigPin, LOW);

  ss.pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH); //, 20000);

  cm = (duration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343
  inches = (duration/2) / 74;   // Divide by 74 or multiply by 0.0135
  
  SPrint(trigPin);
  SPrint(",");
  SPrint(echoPin);
  SPrint("  --   ");
  SPrint(duration);
  SPrint("  --   ");
  SPrint(inches);
  SPrint("in,   ");
  SPrint(cm);
  SPrint("cm");
  SPrintln("");
  
  delay(500);
}

void ultrasonicSensorDetect(int trigPin, int echoPin) {
  long duration = 0;
  long inches = 0;
  long cm = 0;

  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH); //, 20000);

  cm = (duration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343
  inches = (duration/2) / 74;   // Divide by 74 or multiply by 0.0135
  
  SPrint(trigPin);
  SPrint(",");
  SPrint(echoPin);
  SPrint("  --   ");
  SPrint(duration);
  SPrint("  --   ");
  SPrint(inches);
  SPrint("in,   ");
  SPrint(cm);
  SPrintln("cm");
  
  delay(500);
}

void readBatterySensor() {
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
  
  SPrint("Bus Voltage:   "); SPrint(busvoltage); SPrintln(" V");
  SPrint("Shunt Voltage: "); SPrint(shuntvoltage); SPrintln(" mV");
  SPrint("Load Voltage:  "); SPrint(loadvoltage); SPrintln(" V");
  SPrint("Current:       "); SPrint(current_mA); SPrintln(" mA");
  SPrint("Power:         "); SPrint(power_mW); SPrintln(" mW");
  SPrintln("");

  delay(2000);
}

//Private Functions
