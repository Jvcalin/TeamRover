

#define speakerPin 18 //A0 //0
 
//int numTones = 10;
//int tones[] = {261, 277, 294, 311, 330, 349, 370, 392, 415, 440};
//            mid C  C#   D    D#   E    F    F#   G    G#   A

#define  Ct  261
#define  Cst  277
#define  Dt  294
#define  Dst  311
#define  Et  330
#define  Ft  349
#define  Fst  370
#define  Gt  392
#define  Gst  415
#define  At  440

#define EIGHTH 1
#define QUARTER  2
#define HALF  4
#define WHOLE  8
#define OCTAVE 2

int tempo = 250;
//https://techtutorialsx.com/2017/07/01/esp32-arduino-controlling-a-buzzer-with-pwm/

void SetupSounds() {
  SPrintln("Sound Setup");
  //pinMode(speakerPin, OUTPUT);
  ledcSetup(0,1E5,12);
  ledcAttachPin(speakerPin,0);
  //PlayTone();
  PlayBeep();
}

//void SwitchToSound() {
//  SPrintln("Switch to Sound");
//  pinMode(speakerPin, OUTPUT);
//}

//void SwitchToInterrupt() {
//  SPrintln("Switch to Interrupt");
//  pinMode(speakerPin, INPUT);
//}

//void PlayTone() {
//  for (int i = 0; i < numTones; i++)
//  {
//    tone(speakerPin, tones[i]);
//    delay(500);
//  }
//  noTone(speakerPin);
//}

void Play(const char* cmd) {
  if (strcmp(cmd,"SwoopUp") == 0)
    PlaySwoopUp();
  else if (strcmp(cmd,"SwoopDown") == 0)
    PlaySwoopDown();
  else if (strcmp(cmd,"Beep") == 0)
    PlayBeep();
  else if (strcmp(cmd,"DeepBeep") == 0)
    PlayDeepBeep();
  else if (strcmp(cmd,"DuntDuntDunt") == 0)
    PlayDuntDuntDunt();
  else
    SPrint("unknown beep cmd"); 
}

void Play(String cmd) {
  if (cmd.equals("SwoopUp"))
    PlaySwoopUp();
  else if (cmd.equals("SwoopDown"))
    PlaySwoopDown();
  else if (cmd.equals("Beep"))
    PlayBeep();
  else if (cmd.equals("DeepBeep"))
    PlayDeepBeep();
  else if (cmd.equals("DuntDuntDunt"))
    PlayDuntDuntDunt();
  else
    SPrintln("unknown beep cmd"); 
}

void PlaySwoopUp() {
  //261 - 440

  float t=0;
  for (int i = 0; t < 440; i++){
    t = (i*i * 0.75) + 261 ;
    //tone(speakerPin, round(t));
    ledcWriteTone(0, round(t));
    //SPrintln(t);
    delay(50);
  }
  //noTone(speakerPin);
  ledcWriteTone(0,0);
}

void PlayBeep() {
  SPrintln("PlayBeep!");
  PlayGs(QUARTER);
}

void PlayDeepBeep() {
  PlayC(QUARTER);
}

void PlaySwoopDown() {
  //261 - 440

  float t=440;
  for (int i = 0; t > 261; i++){
    t = 440 - (i*i * 0.75);
    //tone(speakerPin, round(t));
    ledcWriteTone(0, round(t));
    //SPrintln(t);
    delay(50);
  }
  //noTone(speakerPin);
  ledcWriteTone(0,0);
}

void PlayDuntDuntDunt() {
  //SwitchToSound();
  SPrintln("DuntDuntDunt!");
  PlayF(QUARTER);
  PlayRest(EIGHTH);
  PlayC(QUARTER);
  PlayRest(EIGHTH);
  PlayA(WHOLE);

  //SwitchToInterrupt();
}

void PlayRest(int tlength) {
  ledcWriteTone(0,0);
  delay(tlength * tempo);
}

void PlayC(int tlength) {
  ledcWriteNote(0,NOTE_C,OCTAVE);
  //tone(speakerPin, Ct);
  delay(tlength * tempo);
  //noTone(speakerPin);
  ledcWriteTone(0,0);
}

void PlayCs(int tlength) {
  ledcWriteNote(0,NOTE_Cs,OCTAVE);
  //tone(speakerPin, Cst);
  delay(tlength * tempo);
  //noTone(speakerPin);
  ledcWriteTone(0,0);
}

void PlayD(int tlength) {
  ledcWriteNote(0,NOTE_D,OCTAVE);
  //tone(speakerPin, Dt);
  delay(tlength * tempo);
  //noTone(speakerPin);
  ledcWriteTone(0,0);
}

void PlayEb(int tlength) {
  ledcWriteNote(0,NOTE_Eb,OCTAVE);
  //tone(speakerPin, Dst);
  delay(tlength * tempo);
  //noTone(speakerPin);
  ledcWriteTone(0,0);
}

void PlayE(int tlength) {
  ledcWriteNote(0,NOTE_E,OCTAVE);
  //tone(speakerPin, Et);
  delay(tlength * tempo);
  //noTone(speakerPin);
  ledcWriteTone(0,0);
}

void PlayF(int tlength) {
  ledcWriteNote(0,NOTE_F,OCTAVE);
  //tone(speakerPin, Ft);
  delay(tlength * tempo);
  //noTone(speakerPin);
  ledcWriteTone(0,0);
}

void PlayFs(int tlength) {
  ledcWriteNote(0,NOTE_Fs,OCTAVE);
  //tone(speakerPin, Fst);
  delay(tlength * tempo);
  //noTone(speakerPin);
  ledcWriteTone(0,0);
}

void PlayG(int tlength) {
  ledcWriteNote(0,NOTE_G,OCTAVE);
  //tone(speakerPin, Gt);
  delay(tlength * tempo);
  //noTone(speakerPin);
  ledcWriteTone(0,0);
}

void PlayGs(int tlength) {
  ledcWriteNote(0,NOTE_Gs,OCTAVE);
  //tone(speakerPin, Gst);
  delay(tlength * tempo);
  //noTone(speakerPin);
  ledcWriteTone(0,0);
}

void PlayA(int tlength) {
  ledcWriteNote(0,NOTE_A,OCTAVE);
  //tone(speakerPin, At);
  delay(tlength * tempo);
  //noTone(speakerPin);
  ledcWriteTone(0,0);
}

void PlayBb(int tlength) {
  ledcWriteNote(0,NOTE_Bb,OCTAVE);
  //tone(speakerPin, At);
  delay(tlength * tempo);
  //noTone(speakerPin);
  ledcWriteTone(0,0);
}

void PlayB(int tlength) {
  ledcWriteNote(0,NOTE_B,OCTAVE);
  //tone(speakerPin, At);
  delay(tlength * tempo);
  //noTone(speakerPin);
  ledcWriteTone(0,0);
}
