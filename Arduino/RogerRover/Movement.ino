
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

#define isTOUCHING 111
#define isCLOSE 222
#define isNEAR 333
#define isMEDIUM 444
#define isFAR 555
#define isNOSIGNAL 000

int currentAction = mSTOP;
int waitTimer = 0;
bool spinning = false;

int getDistance(int dist) {
  if (dist > dNOSIGNAL)
    return dNOSIGNAL;
  else if (dist > dFAR)
    return dFAR;
  else if (dist > dMEDIUM)
    return dMEDIUM;
  else if (dist > dNEAR)
    return dNEAR;
  else if (dist > dCLOSE)
    return dCLOSE;
  else
    return dTOUCHING;
}


bool IsOff() {
  return currentAction == mOFF;
}

void ActionOff() {
  //nothing
  currentAction = mOFF;
}


void GoStop(int wait = 0) {
  waitTimer = wait;
  currentAction = mSTOP;
}

void ActionStop() {
  
  if (currSpeed > 0 || currentAction != mSTOP) {
    stopRun();
    GoStop();
    return;
  }

  if (waitTimer > 0) {
    waitTimer--;
    return;
  }
    
  if (getDistance(fDistance) == isCLOSE && getDistance(bDistance) == isCLOSE) {
    //Both front and back are covered
    GoOff();
    PlaySwoopDown();
    SPrintln("OFF");
  } else if (getDistance(fDistance) == isTOUCHING) {
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
  } else if (getDistance(fDistance) == isCLOSE) {
    //Default movement
    GoForward();
  }  
}

void ActionForward() {
  
  if (getDistance(fDistance) <= isCLOSE || getDistance(lDistance) <= isCLOSE || getDistance(rDistance) <= isCLOSE) {
    //About to collide
    PlayBeep();
    GoStop(50);
    return;
  }

  if (currSpeed == 0 || currentAction != mFORWARD) {
    goForward();
    waitTimer = 50;  
    GoForward();
  }

  if (waitTimer > 0) {
    waitTimer--;
    return;
  }

  //if (getDistance(rDistance) == isCLOSE && getDistance(fDistance) == isNEAR && getDistance(lDistance) == isNEAR) {
  //  goLeft(2);
  //} else if (getDistance(rDistance) == isCLOSE && getDistance(fDistance) == isNEAR && getDistance(lDistance) == isNEAR) {
  //  goRight(2);
  //}

      
  if (getDistance(fDistance) >= isFAR) {
    //No objects immediately ahead
    if (currSpeed < MAX_SPEED) {
      goFaster();
      waitTimer = 100;  
    } 
  } else if (getDistance(fDistance) <= isMEDIUM) {
    //Object close
    if (currSpeed > 2) {
      goSlower();
      waitTimer = 20;
    }
  } else if (getDistance(fDistance) <= isNEAR) {
    //Object very close
    if (currSpeed > 1) {
      goSlower();
    }
  } 
}

void ActionSpinLeft() {

  if (!spinning) {
    spinLeft(3);
    spinning = true;
  }

  if (getDistance(fDistance) >= isNEAR && getDistance(rDistance) >= isNEAR && getDistance(lDistance) >= isNEAR) {
    spinning = false;
    GoStop(25);
  }
}

void ActionSpinRight() {
  
  if (!spinning) {
    spinRight(3);
    spinning = true;
  }

  if (getDistance(fDistance) >= isNEAR && getDistance(rDistance) >= isNEAR && getDistance(lDistance) >= isNEAR) {
    spinning = false;
    GoStop(25);
  }  
}

void ActionReverse() {
  
  if (currSpeed == 0) {
    goReverse();
  }
  
  if (waitTimer > 0) {
    waitTimer--;
    return;
  }
      
  if (getDistance(bDistance) <= isCLOSE) {
    GoStop(30);
  } else if (getDistance(fDistance) >= isMEDIUM) {
    if (lDistance >= rDistance) 
      GoSpinLeft();
    else if (rDistance > lDistance)
      GoSpinRight(); 
  } else if (currSpeed > -2 && currSpeed > MIN_SPEED) {
    goFaster();
    waitTimer = 50;
  }
}



void MotorsTick() {

  if (getDistance(fDistance) == isNOSIGNAL)
    fDistance = (rDistance + lDistance);// 2;

  if (getDistance(rDistance) == isNOSIGNAL)
    rDistance = (fDistance + lDistance);// 2;

  if (getDistance(lDistance) > dNOSIGNAL)
    lDistance = (rDistance + fDistance);// 2;
  
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
      ActionStop();
      break;
  }
  
}

void GoOff() {
  currentAction = mOFF;
}

void GoForward() {
  currentAction = mFORWARD;
}

void GoSpinLeft() {
  currentAction = mSPINLEFT;
}

void GoSpinRight() {
  currentAction = mSPINRIGHT;
}

void GoReverse() {
  currentAction = mREVERSING;
}
