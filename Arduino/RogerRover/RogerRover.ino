//Main Module

//I2C Addresses
//PWMServoDriver -- 0x40
//MotorShield -- 0x60
//OLED -- 0x3C  //cannot change
//INA219 Featherwing -- 0x41   -- 0x40 (no jumpers) -- !!! --0x41 (A0) --0x44 (A1)  --0x45 (A0 & A1)
//INA219 basic 0x44 ??
//Seesaw 0x49
//Seesaw 0x4A

//Pin Assignments ESP8266
//A0 - piezo buzzer
//14
//12 - white  ultrasonic front echo
//13 - gray  ultrasonic right echo
//15 - purple  ultrasonic back echo
//0 - Red LED
//16 - black  ultrasonic left echo
//2 - OLED Button C - seesaw interrupt

//Pin Assignments ESP32
//13/A12 - Red LED
//12/A11
//27/A10
//33/A9
//15/A8 - OLED Button A
//32/A7 - OLED Button B
//14/A6 - OLED Button C

//A0/DAC2 - piezo buzzer
//A1/DAC1
//A2/34
//A3/39
//A4/36
//A5/4
//SCK/5
//MOSI/18
//MISO/19
//RX/16
//TX/17
//21

//A13 - Voltage level

//Seesaw Pin Assignments
//GPIO/Neopixel
//9  piezo vib sensor
//10 - yellow  ultrasonic left trig
//11 - orange  ultrasonic front trig
//14 - red  ultrasonic right trig
//15 - brown  ultrasonic back trig
//24 - piezo vib sensor
//25 - neopixel
//Analog Pins
//2
//3
//4
//PWM Pins
//5
//6
//7
// Seesaw 2
//GPIO/Neopixel
//9  
//10 
//11 
//14 
//15 
//24 
//25 
//Analog Pins
//2
//3
//4
//PWM Pins
//5
//6
//7
#define redLed 13 //0

long timer = 0;
long timer1 = 50;

int fDistance = 50;
int bDistance = 50;
int lDistance = 50;
int rDistance = 50;

int redLedState = HIGH;

void setup() {
Serial.begin(115200); 


  pinMode(redLed, OUTPUT);
  blinkRedLED();
  delay(1000);
  blinkRedLED();
  delay(1000);
  blinkRedLED();
  delay(1000); 

  //attachInterrupt(digitalPinToInterrupt(BUTTON_A), DoButtonA, RISING);
  //attachInterrupt(digitalPinToInterrupt(BUTTON_B), DoButtonB, RISING);
  //attachInterrupt(digitalPinToInterrupt(BUTTON_C), DoButtonC, RISING);
//LOW to trigger the interrupt whenever the pin is low,
//CHANGE to trigger the interrupt whenever the pin changes value
//RISING to trigger when the pin goes from low to high,
//FALLING for when the pin goes from high to low.
  SetupSerial();
  delay(1000);
  //SetupSensors();
  delay(1000);
  SetupMotors();
  delay(1000);
  //SetupSounds();
  delay(1000);
  //SetupServos();
  delay(1000);
  //SetupWiFi();
  delay(1000);
  
//Serial.println("Start Program");  
SPrintln("Starting Program");

//PlayTone();
//PlayDuntDuntDunt();
//delay(1000);
//PlaySwoopUp();
//delay(1000);
//PlaySwoopDown();
//delay(2000);

//PlaySwoopUp();
}

void loop() {
  long startLoop = millis();

  if (timer1 > 50 && true && !IsOff()) {
    timer1 = 0;
  
    //printUltrasonicSensorReadings();
    //readBatterySensor();
  
    redLedState = FlipValue(redLedState);
    pinMode(redLed, OUTPUT);
    digitalWrite(redLed, redLedState);

    WiFiTick();  
  }

  //SensorsTick();
 
  MotorsTick();
  //SenseVibration();
  //ServoTick();
  delay(10);
   
  long timeElapsed = millis() - startLoop;
  //SPrint("Loop:");
  //SPrint(timeElapsed);
  //SPrint("ms ");
  //SPrintln(timer); 

  timer++;
  timer1++;  
}



void testloop() {
  // put your main code here, to run repeatedly:
  //SPrintln("Starting the loop");
  long startLoop = millis();

  //blinkRedLED();

  //TestServo();
  //TestMotor();
  //motorSpeedTest();
  //backMotorSpeedTest();
  //IndividualWheelTest();
  //return;
  
  //OLEDTick();
  //ServoTick();

//IR Optical Sensor (Close)
//bool detect = OpSensorDetect();
//if (detect) {
//  SPrintln("Detected HIGH");
//}
//else {
//  SPrintln("Detected LOW");
//}

//delay(250);

//Ultrasonic Sensor
if (timer1 > 50 && true && !IsOff()) {
  timer1 = 0;

  printUltrasonicSensorReadings();
  //readBatterySensor();

  redLedState = FlipValue(redLedState);
  pinMode(redLed, OUTPUT);
  digitalWrite(redLed, redLedState);
}

  SensorsTick();
 
  delay(10);
  
  MotorsTick();
  //SenseVibration();

  WiFiTick();


  long timeElapsed = millis() - startLoop;
  //SPrint("Loop:");
  //SPrint(timeElapsed);
  //SPrint("ms ");
  //SPrintln(timer); 

  timer++;
  timer1++;
}
