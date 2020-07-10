
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
    
  //if (getDistance(getFrontDistance()) == isTOUCHING && getDistance(getBackDistance()) == isTOUCHING) {
  //  //Both front and back are covered
  //  GoOff();
  //  PlaySwoopDown();
  //  SPrintln("OFF");
  //}
  
  /*   else if (getDistance(getFrontDistance()) == isTOUCHING) {
    //Hit something
    GoReverse();
  } else if (getDistance(getFrontDistance()) == isCLOSE && getDistance(getRightDistance()) == isCLOSE && getDistance(getLeftDistance()) == isCLOSE) {
    //Closed on three sides
    GoReverse();
  } else if (getDistance(getFrontDistance()) == isCLOSE) {  
    //Stopped at wall
    if (getLeftDistance() >= getRightDistance()) 
      GoSpinLeft(); 
    else if (getRightDistance() > getLeftDistance())
      GoSpinRight();   
  } else if (getDistance(getBackDistance()) == isCLOSE) {
    //Wall behind
    GoForward();
  } else if (getDistance(getFrontDistance()) > isCLOSE) {
    //Default movement
    GoForward();
  }  */
}

void ActionForward() {
  
  //if (getDistance(getFrontDistance()) <= isCLOSE || getDistance(getLeftDistance()) <= isCLOSE || getDistance(getRightDistance()) <= isCLOSE) {
  //  //About to collide
  //  PlayBeep();
  //  GoStop(50);
  //  return;
  //}

  if (getCurrSpeed() == 0 || currentAction != mFORWARD) {
    goForward();
    waitTimer = 50;  
    GoForward();
  }

  //if (waitTimer > 0) {
  //  waitTimer--;
  //  return;
  //}

  //if (getDistance(getRightDistance()) == isCLOSE && getDistance(getFrontDistance()) == isNEAR && getDistance(getLeftDistance()) == isNEAR) {
  //  goLeft(2);
  //} else if (getDistance(getRightDistance()) == isCLOSE && getDistance(getFrontDistance()) == isNEAR && getDistance(getLeftDistance()) == isNEAR) {
  //  goRight(2);
  //}

      
  //if (getDistance(getFrontDistance()) >= isFAR) {
  //  //No objects immediately ahead
  //  if (getCurrSpeed() < MAX_SPEED) {
  //    goFaster();
  //    waitTimer = 100;  
  //  } 
  //} else if (getDistance(getFrontDistance()) <= isMEDIUM) {
  //  //Object close
  //  if (getCurrSpeed() > 2) {
  //    goSlower();
  //    waitTimer = 20;
  //  }
  //} else if (getDistance(getFrontDistance()) <= isNEAR) {
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
  //if (getDistance(getFrontDistance()) == isTOUCHING && getDistance(getBackDistance()) == isTOUCHING) {
  //  //Both front and back are covered
  //  GoOff();
  //  PlaySwoopDown();
  //  SPrintln("OFF");
  //}
  //if (getDistance(getFrontDistance()) >= isNEAR && getDistance(getRightDistance()) >= isNEAR && getDistance(getLeftDistance()) >= isNEAR) {
  //  spinning = false;
  //  GoStop(25);
  //}
}

void ActionSpinRight() {
  
  if (!spinning) {
    spinRight(3);
    spinning = true;
  }
  //if (getDistance(getFrontDistance()) == isTOUCHING && getDistance(getBackDistance()) == isTOUCHING) {
  //  //Both front and back are covered
  //  GoOff();
  //  PlaySwoopDown();
  //  SPrintln("OFF");
  //}
  //if (getDistance(getFrontDistance()) >= isNEAR && getDistance(getRightDistance()) >= isNEAR && getDistance(getLeftDistance()) >= isNEAR) {
  //  spinning = false;
  //  GoStop(25);
  //}  
}

void ActionTurnLeft() {
  if (getCurrSpeed() <= 0) {
    goForward();
  }
  goLeft(1);
}

void ActionTurnRight() {
  if (getCurrSpeed() <= 0) {
    goForward();
  }
  goRight(1);
}

void ActionReverse() {
  
  if (getCurrSpeed() == 0) {
    goReverse();
  }
  
  //if (getDistance(getFrontDistance()) == isTOUCHING && getDistance(getBackDistance()) == isTOUCHING) {
  //  //Both front and back are covered
  //  GoOff();
  //  PlaySwoopDown();
  //  SPrintln("OFF");
  //}

  //if (getDistance(getBackDistance()) <= isCLOSE) {
  //  GoStop(30);
  //}
  
  //if (waitTimer > 0) {
  //  waitTimer--;
  //  return;
  //}
      
  //if (getDistance(getBackDistance()) <= isCLOSE) {
  //  GoStop(30);
  //} else if (getDistance(getFrontDistance()) >= isMEDIUM) {
  //  if (getLeftDistance() >= getRightDistance()) 
  //    GoSpinLeft();
  //  else if (getRightDistance() > getLeftDistance())
  //    GoSpinRight(); 
  //} else if (getCurrSpeed() > -2 && getCurrSpeed() > MIN_SPEED) {
  //  goFaster();
  //  waitTimer = 50;
  //}
}

void ActionReverseLeft() {
  if (getCurrSpeed() >= 0) {
    goReverse();
  }
  goLeft(1);
}

void ActionReverseRight() {
  if (getCurrSpeed() >= 0) {
    goReverse();
  }
  goRight(1);
}

void MotorsTick() {
  //SPrint(currentAction);
  //SPrint(" ");
  //SPrintln(getCurrSpeed());

  //if (getDistance(getFrontDistance()) > isNOSIGNAL)
  //  getFrontDistance() = -1; //(getRightDistance() + getLeftDistance());// 2;

  //if (getDistance(getRightDistance()) > isNOSIGNAL)
  //  getRightDistance() = -1; //(getFrontDistance() + getLeftDistance());// 2;

  //if (getDistance(getLeftDistance()) > dNOSIGNAL)
  //  getLeftDistance() = -1; //(getRightDistance() + getFrontDistance());// 2;

  //if (getDistance(getBackDistance()) > dNOSIGNAL)
  //  getBackDistance() = -1;
    
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
    case mTURNINGLEFT:
      ActionTurnLeft();
      break;
    case mTURNINGRIGHT:
      ActionTurnRight();
      break;
    case mREVERSINGLEFT:
      ActionReverseLeft();
      break;
    case mREVERSINGRIGHT:
      ActionReverseRight();
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
    case mTURNINGLEFT:
      return "TurnLeft";
      break;
    case mTURNINGRIGHT:
      return "TurnRight";
      break;
    case mREVERSINGLEFT:
      return "ReverseLeft";
      break;
    case mREVERSINGRIGHT:
      return "ReverseRight";
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
  else if (strcmp(command, "TurnLeft")==0)
      GoTurnLeft();
  else if (strcmp(command, "TurnRight")==0)
      GoTurnRight();
  else if (strcmp(command, "ReverseLeft")==0) 
      GoReverseLeft();
  else if (strcmp(command, "ReverseRight")==0) 
      GoReverseRight();
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
  else if (command.equals("TurnLeft"))
      GoTurnLeft();
  else if (command.equals("TurnRight"))
      GoTurnRight();
  else if (command.equals("ReverseLeft")) 
      GoReverseLeft();
  else if (command.equals("ReverseRight")) 
      GoReverseRight();
  else if (command.equals("Stop"))
      GoStop();
  else if (command.equals("GoFaster")) 
      goFaster();
  else if (command.equals("GoSlower")) {
      goSlower();
      if (getCurrSpeed() == 0)
        GoStop();    
  }
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

void GoTurnLeft() {
  SPrintln("ActionTurnLeft");
  currentAction = mTURNINGLEFT;
}

void GoTurnRight() {
  SPrintln("ActionTurnRight");
  currentAction = mTURNINGRIGHT;
}

void GoReverseLeft() {
  SPrintln("ActionReverseLeft");
  currentAction = mREVERSINGLEFT;
}

void GoReverseRight() {
  SPrintln("ActionReverseRight");
  currentAction = mREVERSINGRIGHT;
}
