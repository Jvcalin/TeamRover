//Main Module
#if defined(ESP8266)
  #define BUTTON_A  0
  #define BUTTON_B 16
  #define BUTTON_C  2
#elif defined(ESP32)
  #define BUTTON_A 15
  #define BUTTON_B 32
  #define BUTTON_C 14
#endif

//I2C Addresses
//PWMServoDriver -- 0x40
//MotorShield -- 0x60
//OLED -- 0x3C  //cannot change
//INA219 Featherwing -- 0x41   -- 0x40 (no jumpers) -- !!! --0x41 (A0) --0x44 (A1)  --0x45 (A0 & A1)
//INA219 basic 0x44 ??
//Seesaw 0x49

//Pin Assignments
//A0
//14 - black  ultrasonic front echo
//12 - white  ultrasonic front trig
//13 - gray  ultrasonic back  echo
//15 - purple  ultrasonic back  trig
//0 - OLED Button A
//16 - OLED Button B
//2 - OLED Button C

//Seesaw Pin Assignments
//GPIO/Neopixel
//9  piezo buzzer
//10 - yellow  ultrasonic left echo
//11 - orange  ultrasonic left trig
//14 - red  ultrasonic right echo
//15 - brown  ultrasonic right trig
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

long timer = 0;

void setup() {
Serial.begin(115200); 

  //attachInterrupt(digitalPinToInterrupt(BUTTON_A), DoButtonA, RISING);
  //attachInterrupt(digitalPinToInterrupt(BUTTON_B), DoButtonB, RISING);
  //attachInterrupt(digitalPinToInterrupt(BUTTON_C), DoButtonC, RISING);
//LOW to trigger the interrupt whenever the pin is low,
//CHANGE to trigger the interrupt whenever the pin changes value
//RISING to trigger when the pin goes from low to high,
//FALLING for when the pin goes from high to low.
  
  //SetupSerial();
  delay(1000);
  //SetupServos();
  delay(1000);
  //SetupMotors();
  delay(1000);
  SetupSensors();
  delay(1000);
  //SetupWifi();

  
SPrintln("Start Program");

//PlayTone();
//PlayDuntDuntDunt();
//delay(1000);
//PlaySwoopUp();
//delay(1000);
//PlaySwoopDown();
//delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:
  //SPrintln("Starting the loop");
  long startLoop = millis();

  //TestServo();
  //TestMotor();
  
  //OLEDTick();
  //ServoTick();


//Test Prox Sensors

//IR Optical Sensor (Close)
//bool detect = OpSensorDetect();
//if (detect) {
//  SPrintln("Detected HIGH");
//}
//else {
//  SPrintln("Detected LOW");
//}

delay(250);

//Ultrasonic Sensor
ultrasonicSensorDetectFront();
ultrasonicSensorDetectBack();

  delay(1);
  
  long timeElapsed = millis() - startLoop;
  //SPrint("Loop:");
  //SPrint(timeElapsed);
  //SPrint("ms ");
  //SPrintln(timer); 

  timer++;
  if (timer > 30000)
    timer = 0;
}

void TestMotor() {
  switch (timer) {
    case 3000:
      goStraight();
      //motorMove(1);
      break;
    case 6000:
      veerLeft();
      break;
    case 9000:
      goStraight();
      //motorMove(2);
      break;
    case 12000:
      veerRight();
      //motorMove(3);
      break;
    case 15000:
      goStraight();
      //motorMove(4);
      break;
    case 18000:
      stopRun();
      //motorMove(5);
      break;
    case 21000:
      goReverse();
      //motorMove(2);
      break;
    case 24000:
      goReverse();
      break;      
    case 27000:
      stopRun();
      break;  
    default:
      break;
  }
  
}

void TestServo() {

  switch (timer) {
    case 0:
      ResetServos();
      break;
    case 3000:
      ServoMoveLeft(45);
      break;
    case 6000:
      ServoMoveUp(40);
      break;
    case 9000:
      ServoMoveDown(80);
      break;
    case 12000:
      ServoMoveRight(90);
      break;
    case 15000:
      ServoMoveLeft(45);
      break;
    case 18000:
      ServoMoveUp(40);
      break;
    case 21000:
      ResetServos();
      break;
    default:
      break;
  }

}
