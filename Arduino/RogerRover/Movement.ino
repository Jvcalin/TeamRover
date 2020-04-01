
#define mOFF 0
#define mSTOP 1
#define mFORWARD 2
#define mSPINLEFT 3
#define mSPINRIGHT 4
#define mREVERSING 5
#define mTURNINGLEFT 6
#define mTURNINGRIGHT 7
#define mREVERSINGLEFT 8
#define mREVERSINGRIGHT 9

#define dTOUCHING 1
#define dCLOSE 6
#define dNEAR 18
#define dMEDIUM 32
#define dFAR 48
#define dNOSIGNAL 300

#define isTOUCHING 10
#define isCLOSE 20
#define isNEAR 30
#define isMEDIUM 40
#define isFAR 50
#define isNOSIGNAL 99

int currentAction = mSTOP;
int waitTimer = 100;
bool spinning = false;

int getDistance(int dist) {
  if (dist > dNOSIGNAL)
    return isNOSIGNAL;
  else if (dist > dFAR)
    return isFAR;
  else if (dist > dMEDIUM)
    return isMEDIUM;
  else if (dist > dNEAR)
    return isNEAR;
  else if (dist > dCLOSE)
    return isCLOSE;
  else
    return isTOUCHING;
}


bool IsOff() {
  return currentAction == mOFF;
}

void ActionOff() {
  //nothing
  currentAction = mOFF;
}


void GoStop(int wait = 0) {
  currentAction = mSTOP;
  SPrintln("ActionStop!!!");
  waitTimer = wait;
  spinning = false;
  stopRun();
}

void ActionStop() {
  //SPrint(currentAction);
  //SPrint(" ");
  //SPrintln(getCurrSpeed());
    
  if (getCurrSpeed() != 0 || spinning || currentAction != mSTOP){ 
    SPrintln("I'm trying to stop!");
    stopRun();
    GoStop();
    return;
  }

  if (waitTimer > 0) {
    waitTimer--;
    return;
  }
    
  //if (getDistance(fDistance) == isTOUCHING && getDistance(bDistance) == isTOUCHING) {
  //  //Both front and back are covered
  //  GoOff();
  //  PlaySwoopDown();
  //  SPrintln("OFF");
  //}
  
  /*   else if (getDistance(fDistance) == isTOUCHING) {
    //Hit something
    GoReverse();
  } else if (getDistance(fDistance) == isCLOSE && getDistance(rDistance) == isCLOSE && getDistance(lDistance) == isCLOSE) {
    //Closed on three sides
    GoReverse();
  } else if (getDistance(fDistance) == isCLOSE) {  
    //Stopped at wall
    if (lDistance >= rDistance) 
      GoSpinLeft(); 
    else if (rDistance > lDistance)
      GoSpinRight();   
  } else if (getDistance(bDistance) == isCLOSE) {
    //Wall behind
    GoForward();
  } else if (getDistance(fDistance) > isCLOSE) {
    //Default movement
    GoForward();
  }  */
}

void ActionForward() {
  
  if (getDistance(fDistance) <= isCLOSE || getDistance(lDistance) <= isCLOSE || getDistance(rDistance) <= isCLOSE) {
    //About to collide
    PlayBeep();
    GoStop(50);
    return;
  }

  if (getCurrSpeed() == 0 || currentAction != mFORWARD) {
    goForward();
    waitTimer = 50;  
    GoForward();
  }

  //if (waitTimer > 0) {
  //  waitTimer--;
  //  return;
  //}

  //if (getDistance(rDistance) == isCLOSE && getDistance(fDistance) == isNEAR && getDistance(lDistance) == isNEAR) {
  //  goLeft(2);
  //} else if (getDistance(rDistance) == isCLOSE && getDistance(fDistance) == isNEAR && getDistance(lDistance) == isNEAR) {
  //  goRight(2);
  //}

      
  //if (getDistance(fDistance) >= isFAR) {
  //  //No objects immediately ahead
  //  if (getCurrSpeed() < MAX_SPEED) {
  //    goFaster();
  //    waitTimer = 100;  
  //  } 
  //} else if (getDistance(fDistance) <= isMEDIUM) {
  //  //Object close
  //  if (getCurrSpeed() > 2) {
  //    goSlower();
  //    waitTimer = 20;
  //  }
  //} else if (getDistance(fDistance) <= isNEAR) {
  //  //Object very close
  //  if (getCurrSpeed() > 1) {
  //    goSlower();
  //  }
  //} 
}

void ActionSpinLeft() {

  if (!spinning) {
    spinLeft(3);
    spinning = true;
  }
  if (getDistance(fDistance) == isTOUCHING && getDistance(bDistance) == isTOUCHING) {
    //Both front and back are covered
    GoOff();
    PlaySwoopDown();
    SPrintln("OFF");
  }
  //if (getDistance(fDistance) >= isNEAR && getDistance(rDistance) >= isNEAR && getDistance(lDistance) >= isNEAR) {
  //  spinning = false;
  //  GoStop(25);
  //}
}

void ActionSpinRight() {
  
  if (!spinning) {
    spinRight(3);
    spinning = true;
  }
  if (getDistance(fDistance) == isTOUCHING && getDistance(bDistance) == isTOUCHING) {
    //Both front and back are covered
    GoOff();
    PlaySwoopDown();
    SPrintln("OFF");
  }
  //if (getDistance(fDistance) >= isNEAR && getDistance(rDistance) >= isNEAR && getDistance(lDistance) >= isNEAR) {
  //  spinning = false;
  //  GoStop(25);
  //}  
}

void ActionReverse() {
  
  if (getCurrSpeed() == 0) {
    goReverse();
  }
  
  if (getDistance(fDistance) == isTOUCHING && getDistance(bDistance) == isTOUCHING) {
    //Both front and back are covered
    GoOff();
    PlaySwoopDown();
    SPrintln("OFF");
  }

  if (getDistance(bDistance) <= isCLOSE) {
    GoStop(30);
  }
  
  //if (waitTimer > 0) {
  //  waitTimer--;
  //  return;
  //}
      
  //if (getDistance(bDistance) <= isCLOSE) {
  //  GoStop(30);
  //} else if (getDistance(fDistance) >= isMEDIUM) {
  //  if (lDistance >= rDistance) 
  //    GoSpinLeft();
  //  else if (rDistance > lDistance)
  //    GoSpinRight(); 
  //} else if (getCurrSpeed() > -2 && getCurrSpeed() > MIN_SPEED) {
  //  goFaster();
  //  waitTimer = 50;
  //}
}



void MotorsTick() {
  //SPrint(currentAction);
  //SPrint(" ");
  //SPrintln(getCurrSpeed());

  if (getDistance(fDistance) > isNOSIGNAL)
    fDistance = -1; //(rDistance + lDistance);// 2;

  if (getDistance(rDistance) > isNOSIGNAL)
    rDistance = -1; //(fDistance + lDistance);// 2;

  if (getDistance(lDistance) > dNOSIGNAL)
    lDistance = -1; //(rDistance + fDistance);// 2;

  if (getDistance(bDistance) > dNOSIGNAL)
    bDistance = -1;
    
  switch (currentAction) {
    case mOFF:
      ActionOff();
      break;
    case mFORWARD:
      ActionForward();
      break;
    case mSPINLEFT:
      ActionSpinLeft();
      break;
    case mSPINRIGHT:
      ActionSpinRight();
      break;
    case mREVERSING:
      ActionReverse();
      break;
    case mSTOP:
      //SPrintln("Stopping!");
      ActionStop();
      break;
    default:
      //SPrintln("Stopping!!!!!!!");
      ActionStop();
  }
  
}

char* getCurrentAction() {
  switch (currentAction) {
    case mOFF:
      return "Off";
      break;
    case mFORWARD:
      return "Forward";
      break;
    case mSPINLEFT:
      return "SpinLeft";
      break;
    case mSPINRIGHT:
      return "SpinRight";
      break;
    case mREVERSING:
      return "Reverse";
      break;
    case mSTOP:
      return "Stop";
      break;
  }
}

void SetCurrentAction(const char* command) {
  
  if (strcmp(command, "Off")==0) 
      GoOff();
  else if (strcmp(command, "Forward")==0)
      GoForward();
  else if (strcmp(command, "SpinLeft")==0)
      GoSpinLeft();
  else if (strcmp(command, "SpinRight")==0) 
      GoSpinRight();
  else if (strcmp(command, "Reverse")==0) 
      GoReverse();
  else if (strcmp(command, "Stop")==0) 
      GoStop();
  else
      GoStop();
}

void SetCurrentAction(String command) {
  
  if (command.equals("Off")) 
      GoOff();
  else if (command.equals("Forward"))
      GoForward();
  else if (command.equals("SpinLeft"))
      GoSpinLeft();
  else if (command.equals("SpinRight")) 
      GoSpinRight();
  else if (command.equals("Reverse")) 
      GoReverse();
  else if (command.equals("Stop"))
      GoStop();
  else
      GoStop();
}

void GoOff() {
  SPrintln("ActionOff");
  currentAction = mOFF;
}

void GoForward() {
  SPrintln("ActionForward");
  currentAction = mFORWARD;
}

void GoSpinLeft() {
  SPrintln("ActionSpinLeft");
  currentAction = mSPINLEFT;
}

void GoSpinRight() {
  SPrintln("ActionSpinRight");
  currentAction = mSPINRIGHT;
}

void GoReverse() {
  SPrintln("ActionReverse");
  currentAction = mREVERSING;
}
