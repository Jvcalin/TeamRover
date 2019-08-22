

int speakerPin = 9;
 
int numTones = 10;
int tones[] = {261, 277, 294, 311, 330, 349, 370, 392, 415, 440};
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

int tempo = 250;

void PlayTone() {
  for (int i = 0; i < numTones; i++)
  {
    tone(speakerPin, tones[i]);
    delay(500);
  }
  noTone(speakerPin);
}

void PlaySwoopUp() {
  //261 - 440

  float t=0;
  for (int i = 0; t < 440; i++){
    t = (i*i * 0.75) + 261 ;
    tone(speakerPin, round(t));
    SPrintln(t);
    delay(50);
  }
  noTone(speakerPin);
}

void PlaySwoopDown() {
  //261 - 440

  float t=440;
  for (int i = 0; t > 261; i++){
    t = 440 - (i*i * 0.75);
    tone(speakerPin, round(t));
    SPrintln(t);
    delay(50);
  }
  noTone(speakerPin);
}

void PlayDuntDuntDunt() {
  PlayF(QUARTER);
  PlayRest(EIGHTH);
  PlayC(QUARTER);
  PlayRest(EIGHTH);
  PlayA(WHOLE);
}

void PlayRest(int tlength) {
  delay(tlength * tempo);
}

void PlayC(int tlength) {
  tone(speakerPin, Ct);
  delay(tlength * tempo);
  noTone(speakerPin);
}

void PlayCs(int tlength) {
  tone(speakerPin, Cst);
  delay(tlength * tempo);
  noTone(speakerPin);
}

void PlayD(int tlength) {
  tone(speakerPin, Dt);
  delay(tlength * tempo);
  noTone(speakerPin);
}

void PlayDs(int tlength) {
  tone(speakerPin, Dst);
  delay(tlength * tempo);
  noTone(speakerPin);
}

void PlayE(int tlength) {
  tone(speakerPin, Et);
  delay(tlength * tempo);
  noTone(speakerPin);
}

void PlayF(int tlength) {
  tone(speakerPin, Ft);
  delay(tlength * tempo);
  noTone(speakerPin);
}

void PlayFs(int tlength) {
  tone(speakerPin, Fst);
  delay(tlength * tempo);
  noTone(speakerPin);
}

void PlayG(int tlength) {
  tone(speakerPin, Gt);
  delay(tlength * tempo);
  noTone(speakerPin);
}

void PlayGs(int tlength) {
  tone(speakerPin, Gst);
  delay(tlength * tempo);
  noTone(speakerPin);
}

void PlayA(int tlength) {
  tone(speakerPin, At);
  delay(tlength * tempo);
  noTone(speakerPin);
}
