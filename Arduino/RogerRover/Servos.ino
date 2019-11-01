//Includes
#include <Adafruit_PWMServoDriver.h>

//Private Variables
// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define H_MIN  120 // out of 4096
#define H_MAX  280
#define V_MIN  120 
#define V_MAX  380 

#define H_NUM  0
#define V_NUM  1

int hInitPos = ((H_MAX - H_MIN)/2) + H_MIN;  //Middle
int vInitPos = (V_MAX - V_MIN)/2 + V_MIN;  

int hpos = hInitPos;
int vpos = vInitPos;

int htargetpos = hInitPos;
int vtargetpos = vInitPos;

int8_t hdir = 0; //-1, 0, 1
int8_t vdir = 0;

int8_t hspeed = 2;
int8_t vspeed = 2;


//Public Functions
void SetupServos() {
  pwm.begin();
  ResetServos();
}

void ResetServos() {
  SPrint("Reset:");
  SPrint(hInitPos);
  SPrint(" - ");
  SPrintln(vInitPos);
  pwm.setPWMFreq(60);
  pwm.setPWM(H_NUM, 0, hInitPos);
  pwm.setPWM(V_NUM, 0, vInitPos);  
}

void ServoTick() {

    //Set Direction
    if (htargetpos > hpos)
        hdir = 1;           
    else if (htargetpos < hpos)
        hdir = -1;
    else
        hdir = 0;

    //Change pos
    int oldhpos = hpos;
    hpos = hpos + (hspeed * hdir);
    if (hpos > H_MAX)
      hpos = H_MAX;
    else if (hpos < H_MIN)
      hpos = H_MIN;
  
    //Move towards it
    if (oldhpos != hpos) 
    {
       pwm.setPWM(H_NUM, 0, hpos);
       //SPrint("H Move: ");
       //SPrintln(hpos);    
    }
      
    //Set Direction
    if (vtargetpos > vpos)
        vdir = 1;           
    else if (vtargetpos < vpos)
        vdir = -1;
    else
        vdir = 0;

    //Change pos
    int oldvpos = vpos;
    vpos = vpos + (vspeed * vdir);
    if (vpos > V_MAX)
      vpos = V_MAX;
    else if (vpos < V_MIN)
      vpos = V_MIN;
  
    //Move towards it
    if (oldvpos != vpos) 
    {
       pwm.setPWM(V_NUM, 0, vpos);
       //SPrint("V Move: ");
       //SPrintln(vpos);    
    }
}

void ServoMoveLeft(int xPercent) {
  if (xPercent != 0) {
   double x = (H_MAX - H_MIN) * xPercent / 100; //map(xPercent,0,99,H_MIN,H_MAX);
   htargetpos -= x; 
   CheckHBounds();
   SPrint("Left -> ");
   SPrint(htargetpos);
   SPrint(" by ");
   SPrintln(x);
  }
}

void ServoMoveRight(int xPercent) {
  if (xPercent != 0) {
    double x = (H_MAX - H_MIN) * xPercent / 100; //map(xPercent,0,99,H_MIN,H_MAX);
    htargetpos += x;
    CheckHBounds();
    SPrint("Right -> ");
    SPrint(htargetpos);
    SPrint(" by ");  
    SPrintln(x);
  }
}

void ServoMoveUp (int yPercent) {
  if (yPercent != 0) {
   int x = (V_MAX - V_MIN) * yPercent / 100; //map(yPercent,0,99,V_MIN,V_MAX);
   vtargetpos -= x;
   CheckVBounds(); 
   SPrint("Up -> ");
   SPrint(vtargetpos);
   SPrint(" by ");   
   SPrintln(x);
  }
}

void ServoMoveDown (int yPercent) {
  if (yPercent != 0) {
   int x = (V_MAX - V_MIN) * yPercent / 100; //map(yPercent,0,99,V_MIN,V_MAX);
   vtargetpos += x;
   CheckVBounds();
   SPrint("Down -> ");
   SPrint(vtargetpos); 
   SPrint(" by ");   
   SPrintln(x);
  }
}

void SetServoSpeed(int spd) {
  hspeed = spd;
  vspeed = spd;
}

void SetServoSpeed(int hspd, int vspd) {
  hspeed = hspd;
  vspeed = vspd;
}

//Private Functions
void CheckHBounds() {
   if (htargetpos > H_MAX) 
     htargetpos = H_MAX;
   else if (htargetpos < H_MIN)
     htargetpos = H_MIN;
}

void CheckVBounds() {
   if (vtargetpos > V_MAX) 
     vtargetpos = V_MAX;
   else if (vtargetpos < V_MIN)
     vtargetpos = V_MIN;  
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
