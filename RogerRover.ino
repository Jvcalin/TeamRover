//Main Module

//I2C Addresses
//PWMServoDriver -- 0x40
//MotorShield -- 0x60
//OLED -- 0x3C  //cannot change
//INA219 Featherwing -- 0x40 (no jumpers) -- !!! --0x41 (A0) --0x44 (A1)  --0x45 (A0 & A1)
//INA219 basic??

//Pin Assignments
//A0
//14
//12
//13
//15
//0
//16
//2

long timer = 0;

void setup() {
Serial.begin(115200); 
  
  //SetupSerial();
  delay(1000);
  //SetupServos();
  delay(1000);
  //SetupMotors();
  delay(1000);
  SetupSensors();

Serial.println("Start Program");

//PlayTone();
PlayDuntDuntDunt();
delay(1000);
PlaySwoopUp();
delay(1000);
PlaySwoopDown();
delay(2000);
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
//  Serial.println("Detected HIGH");
//}
//else {
//  Serial.println("Detected LOW");
//}

//delay(250);

//Ultrasonic Sensor
//ultrasonicSensorDetect();


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
      break;
    case 6000:
      veerLeft();
      break;
    case 9000:
      goStraight();
      break;
    case 12000:
      veerRight();
      break;
    case 15000:
      goStraight();
      break;
    case 18000:
      stopRun();
      break;
    case 21000:
      goReverse();
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
