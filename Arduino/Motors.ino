//Includes
#include <Wire.h>
#include <Adafruit_MotorShield.h>
//#include <Adafruit_PWMServoDriver.h>

//Private Variables
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *leftMotor = AFMS.getMotor(1);
Adafruit_DCMotor *rightMotor = AFMS.getMotor(2);

int leftMotorSpeed = 100;
int rightMotorSpeed = 100;

int MAX_SPEED = 255;
int MIN_SPEED = -255;



//Public Functions
void SetupMotors() {
    SPrintln("Starting Motors");
    AFMS.begin();
    leftMotor->setSpeed(leftMotorSpeed);
    rightMotor->setSpeed(rightMotorSpeed);
}

void motorMove(int mSpeed) {

   SPrint("Both: ");
   SPrint(leftMotorSpeed); 
   SPrint(".");
   SPrint(rightMotorSpeed); 
   SPrint("->");    
   SPrintln(mSpeed); 

  if (mSpeed > MAX_SPEED) {
    //do nothing
  } else if (mSpeed > 0) {
    leftMotorSpeed = mSpeed * 50;
    leftMotor->run(FORWARD);
    rightMotorSpeed = mSpeed * 50;
    rightMotor->run(FORWARD);
  } else if (mSpeed == 0) {
    leftMotor->run(RELEASE);
    rightMotor->run(RELEASE);
  } else if (mSpeed < MIN_SPEED) {
    //do nothing
  } else if (mSpeed < 0) {
    leftMotorSpeed = mSpeed * 50 * -1;
    leftMotor->run(BACKWARD);  
    rightMotorSpeed = mSpeed * 50 * -1;
    rightMotor->run(BACKWARD);    
  }
}

void leftMotorMove(int mSpeed) {

   SPrint("Left: ");
   SPrint(leftMotorSpeed); 
   SPrint(".");
   SPrint(rightMotorSpeed); 
   SPrint("->");    
   SPrintln(mSpeed); 
   
  if (mSpeed > MAX_SPEED) {
    //do nothing
  } else if (mSpeed > 0) {
    leftMotorSpeed = mSpeed * 50;
    leftMotor->run(FORWARD);
  } else if (mSpeed == 0) {
    leftMotor->run(RELEASE);
  } else if (mSpeed < MIN_SPEED) {
    //do nothing
  } else if (mSpeed < 0) {
    leftMotorSpeed = mSpeed * 50 * -1;
    leftMotor->run(BACKWARD);    
  }
}

void rightMotorMove(int mSpeed) {

   SPrint("Right: ");
   SPrint(leftMotorSpeed); 
   SPrint(".");
   SPrint(rightMotorSpeed); 
   SPrint("->");    
   SPrintln(mSpeed); 
   
  if (mSpeed > MAX_SPEED) {
    //do nothing
  } else if (mSpeed > 0) {
    rightMotorSpeed = mSpeed * 50;
    rightMotor->run(FORWARD);
  } else if (mSpeed == 0) {
    rightMotor->run(RELEASE);
  } else if (mSpeed < MIN_SPEED) {
    //do nothing
  } else if (mSpeed < 0) {
    rightMotorSpeed = mSpeed * 50 * -1;
    rightMotor->run(BACKWARD);    
  }  
  
}

void veerRight() {
  SPrintln("Veer Right");
  rightMotorMove(-1);
}

void veerLeft() {
  SPrintln("Veer Left");
  leftMotorMove(-1);
}

void stopRun() {
  motorMove(0);
}

void goStraight() {
  motorMove(1);
}

void goReverse() {
  motorMove(-1);
}

//Private Functions
