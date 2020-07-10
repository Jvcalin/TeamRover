//Includes
#include <Wire.h>
#include <Adafruit_MotorShield.h>
//#include <Adafruit_PWMServoDriver.h>

//Private Variables
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *leftMotor = AFMS.getMotor(3);
Adafruit_DCMotor *rightMotor = AFMS.getMotor(2);
Adafruit_DCMotor *lBackMotor = AFMS.getMotor(4);
Adafruit_DCMotor *rBackMotor = AFMS.getMotor(1);

//int leftMotorSpeed = 3;
//int rightMotorSpeed = 3;
int currSpeed = 0;

int MAX_SPEED = 5;
int MIN_SPEED = -5;

int speedIncrement = 50;

//Public Functions
void SetupMotors() {
    SPrintln("Starting Motors");
    AFMS.begin();
    leftMotor->setSpeed(0);
    rightMotor->setSpeed(0);
    lBackMotor->setSpeed(0);
    rBackMotor->setSpeed(0);
}


// Low level functions

int getCurrSpeed() {
  return currSpeed;
}
void motorMove(int mSpeed) {

   SPrint("Both: ");
   SPrint(mSpeed);
   SPrint(" - ");  
   SPrintln(mSpeed);

  if (mSpeed > MAX_SPEED) {
    currSpeed = MAX_SPEED;
  } else if (mSpeed < MIN_SPEED) {
    currSpeed = MIN_SPEED;
  }

  if (mSpeed > 0) 
    mSpeed = mSpeed + 2;
  else if (mSpeed < 0) 
    mSpeed = mSpeed - 2;

  if (mSpeed > MAX_SPEED) {
    mSpeed = MAX_SPEED;
  } else if (mSpeed < MIN_SPEED) {
    mSpeed = MIN_SPEED;
  }
    
  if (mSpeed > 0) {
    leftMotor->setSpeed(mSpeed * speedIncrement);
    leftMotor->run(FORWARD);
    rightMotor->setSpeed(mSpeed * speedIncrement);
    rightMotor->run(FORWARD);
    lBackMotor->setSpeed(mSpeed * speedIncrement);
    lBackMotor->run(FORWARD);
    rBackMotor->setSpeed(mSpeed * speedIncrement);
    rBackMotor->run(FORWARD);
  } else if (mSpeed == 0) {
    leftMotor->setSpeed(0);
    leftMotor->run(RELEASE);
    rightMotor->setSpeed(0);
    rightMotor->run(RELEASE);
    lBackMotor->setSpeed(0);
    lBackMotor->run(RELEASE);
    rBackMotor->setSpeed(0);
    rBackMotor->run(RELEASE);
  } else if (mSpeed < 0) {
    leftMotor->setSpeed(mSpeed * -1 * speedIncrement);
    leftMotor->run(BACKWARD);  
    rightMotor->setSpeed(mSpeed * -1 * speedIncrement);
    rightMotor->run(BACKWARD);
    lBackMotor->setSpeed(mSpeed * -1 * speedIncrement);
    lBackMotor->run(BACKWARD);  
    rBackMotor->setSpeed(mSpeed * -1 * speedIncrement);
    rBackMotor->run(BACKWARD);     
  }
}

void leftMotorMove(int mSpeed) {

   SPrint("Left: ");
   SPrintln(mSpeed); 

  if (mSpeed > 0) 
    mSpeed = mSpeed;
  else if (mSpeed < 0) 
    mSpeed = mSpeed;

  if (mSpeed > MAX_SPEED) {
    mSpeed = MAX_SPEED;
  } else if (mSpeed < MIN_SPEED) {
    mSpeed = MIN_SPEED;
  }

  if (mSpeed > 0) {
    leftMotor->run(FORWARD);
    leftMotor->setSpeed(mSpeed * speedIncrement);
    lBackMotor->run(FORWARD);
    lBackMotor->setSpeed(mSpeed * speedIncrement);
  } else if (mSpeed == 0) {
    leftMotor->run(RELEASE);
    leftMotor->setSpeed(0);
    lBackMotor->run(RELEASE);
    lBackMotor->setSpeed(0);
  } else if (mSpeed < 0) {
    leftMotor->run(BACKWARD);
    leftMotor->setSpeed(mSpeed * -1 * speedIncrement);
    lBackMotor->run(BACKWARD);
    lBackMotor->setSpeed(mSpeed * -1 * speedIncrement);
  }
}

void rightMotorMove(int mSpeed) {

   SPrint("Right: ");
   SPrintln(mSpeed); 

   
  if (mSpeed > 0) 
    mSpeed = mSpeed;
  else if (mSpeed < 0) 
    mSpeed = mSpeed;

  if (mSpeed > MAX_SPEED) {
    mSpeed = MAX_SPEED;
  } else if (mSpeed < MIN_SPEED) {
    mSpeed = MIN_SPEED;
  }

  if (mSpeed > 0) {
    rightMotor->run(FORWARD);
    rightMotor->setSpeed(mSpeed * speedIncrement);
    rBackMotor->run(FORWARD);
    rBackMotor->setSpeed(mSpeed * speedIncrement);
  } else if (mSpeed == 0) {
    rightMotor->run(RELEASE);
    rightMotor->setSpeed(0);
    rBackMotor->run(RELEASE);
    rBackMotor->setSpeed(0);
  } else if (mSpeed < 0) {
    rightMotor->run(BACKWARD);    
    rightMotor->setSpeed(mSpeed * -1 * speedIncrement);
    rBackMotor->run(BACKWARD);    
    rBackMotor->setSpeed(mSpeed * -1 * speedIncrement);
  }  
  
}

//High-Level Functions

void goRight(int n) {
  SPrintln("Go Right");
  //motorMove(currSpeed);
  if ((currSpeed + n) > MAX_SPEED)
  {
    rightMotorMove(currSpeed - n);
    leftMotorMove(currSpeed);
  }
  else if (currSpeed > 0)
  {
    rightMotorMove(currSpeed);  
    leftMotorMove(currSpeed + n);
  }
  else if ((currSpeed - n)  <= MIN_SPEED)
  {
    rightMotorMove(currSpeed + n);  
    leftMotorMove(currSpeed);
  }
  else if (currSpeed < 0)
  {
    rightMotorMove(currSpeed);  
    leftMotorMove(currSpeed - n);
  }

}

void goLeft(int n) {
  SPrintln("Go Left");
  //motorMove(currSpeed);
  if ((currSpeed + n) >= MAX_SPEED)
  {
    leftMotorMove(currSpeed - n);
    //rightMotorMove(currSpeed + n);
  }
  else if (currSpeed > 0)
  {
    leftMotorMove(currSpeed);
    rightMotorMove(currSpeed + n);
  }
  else if ((currSpeed - n) <= MIN_SPEED)
  {
    leftMotorMove(currSpeed + n);  
    rightMotorMove(currSpeed);
  }
  else if (currSpeed < 0)
  {
    leftMotorMove(currSpeed);  
    rightMotorMove(currSpeed - n);
  }
}

void goStraight() {
  SPrintln("Go Straight");
  motorMove(currSpeed);
}

void stopRun() {
  SPrintln("Stop!!!");
  currSpeed = 0;
  motorMove(0);
}

void goFaster() {
  SPrintln("Go Faster");
  if (currSpeed < 0) {
    currSpeed--;
  } else if (currSpeed > 0) {
    currSpeed++;
  } else {};
  motorMove(currSpeed);
}

void goSlower() {
  SPrintln("Go Slower");
  if (currSpeed > 0) {
    currSpeed--;
  } else if (currSpeed < 0) {
    currSpeed++;
  } else {};
  motorMove(currSpeed); 
}

void goForward() {
  SPrintln("Go Forward");
  if (currSpeed <= 0) {
    //if going in reverse, come to a full stop first before going forward
    motorMove(0);
    currSpeed = 2; //initial speed
  } else {
    currSpeed++;
  }
  motorMove(currSpeed);
}

void goReverse() {
  SPrintln("Go Backward");
  if (currSpeed >= 0) {
    //if going forward, come to a full stop first before going in reverse
    motorMove(0);
    currSpeed = -2; //initial speed
  } else {
    currSpeed--;
  }
  motorMove(currSpeed);
}

void spinLeft(int n) {
  stopRun();
  SPrintln("Spin Left");
  leftMotorMove(-n);
  rightMotorMove(n);
}

void spinRight(int n) {
  stopRun();
  SPrintln("Spin Right");
  leftMotorMove(n);
  rightMotorMove(-n);
}




//Test Functions
void IndividualWheelTest() {
  SPrint("Testing left front wheel:  ");
  leftMotor->run(FORWARD);
  for (int i=0; i<250; i=i+50) {
    SPrint(i);
    SPrint(" ");
    leftMotor->setSpeed(i);
    SPrintln(i); 
    delay(2000);
  }  
  SPrintln("");
  leftMotor->run(RELEASE);
  
  SPrint("Testing right front wheel:  ");
  rightMotor->run(FORWARD);
  for (int i=0; i<250; i=i+50) {
    SPrint(i);
    SPrint(" ");
    rightMotor->setSpeed(i);
    SPrintln(i); 
    delay(2000);
  }  
  SPrintln("");  
  rightMotor->run(RELEASE);

  SPrint("Testing left back wheel:  ");
  lBackMotor->run(FORWARD);
  for (int i=0; i<250; i=i+50) {
    SPrint(i);
    SPrint(" ");
    lBackMotor->setSpeed(i);
    SPrintln(i); 
    delay(2000);
  }  
  SPrintln("");  
  lBackMotor->run(RELEASE);

  SPrint("Testing right back wheel:  ");
  rBackMotor->run(FORWARD);
  for (int i=0; i<250; i=i+50) {
    SPrint(i);
    SPrint(" ");
    rBackMotor->setSpeed(i);
    SPrintln(i); 
    delay(2000);
  }  
  SPrintln(""); 
  rBackMotor->run(RELEASE);

}


void motorSpeedTest() {


  leftMotor->run(FORWARD);
  rightMotor->run(FORWARD);

  for (int i=0; i<250; i=i+50) {
    leftMotor->setSpeed(i);
    rightMotor->setSpeed(i);
    SPrintln(i); 
    delay(3000);
  }

  for (int i=250; i>0; i=i-50) {
    leftMotor->setSpeed(i);
    rightMotor->setSpeed(i);
    SPrintln(i); 
    delay(3000);
  }

  leftMotor->run(RELEASE);
  rightMotor->run(RELEASE);
  
  leftMotor->run(BACKWARD);
  rightMotor->run(BACKWARD);

  for (int i=0; i<250; i=i+50) {
    leftMotor->setSpeed(i);
    rightMotor->setSpeed(i);
    SPrintln(i); 
    delay(3000);
  }

  for (int i=250; i>0; i=i-50) {
    leftMotor->setSpeed(i);
    rightMotor->setSpeed(i);
    SPrintln(i); 
    delay(3000);
  }
  
  leftMotor->run(RELEASE);
  rightMotor->run(RELEASE);
}

void backMotorSpeedTest() {

  lBackMotor->run(FORWARD);
  rBackMotor->run(FORWARD);

  for (int i=0; i<250; i=i+50) {
    lBackMotor->setSpeed(i);
    rBackMotor->setSpeed(i);
    SPrintln(i); 
    delay(3000);
  }

  for (int i=250; i>0; i=i-50) {
    lBackMotor->setSpeed(i);
    rBackMotor->setSpeed(i);
    SPrintln(i); 
    delay(3000);
  }

  lBackMotor->run(RELEASE);
  rBackMotor->run(RELEASE);
  
  lBackMotor->run(BACKWARD);
  rBackMotor->run(BACKWARD);

  for (int i=0; i<250; i=i+50) {
    lBackMotor->setSpeed(i);
    rBackMotor->setSpeed(i);
    SPrintln(i); 
    delay(3000);
  }

  for (int i=250; i>0; i=i-50) {
    lBackMotor->setSpeed(i);
    rBackMotor->setSpeed(i);
    SPrintln(i); 
    delay(3000);
  }
  
  lBackMotor->run(RELEASE);
  rBackMotor->run(RELEASE);
}



void TestMotor() {
  switch (timer) {
    case 1:
      goForward();
    case 300:
      goFaster();
      break;
    case 450:
      goSlower();
      break;
    case 600:
      goLeft(2);
      break;
    case 900:
      goStraight();
      break;
    case 1200:
      goRight(2);
      break;
    case 1500:
      goStraight();
      break;
    case 1800:
      goReverse();
      break;
    case 2100:
      goFaster();
      break;
    case 2400:
      goLeft(2);
      break;      
    case 2700:
      goRight(2);
      break;
    case 3000:
      stopRun();
      break;   
    case 3300:
      spinRight(3);
      break; 
    case 4200:
      spinLeft(3);
      break; 
    case 5100:
      stopRun();
      break; 
    case 5300:
      timer = 0;;
      break; 
    default:
      break;
  }
  
}
