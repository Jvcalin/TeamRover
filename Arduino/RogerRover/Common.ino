//These are common functions used by everyone

#define DEBUG true
#define OLED true

void SetupSerial(){
   Serial.begin(115200);
   Serial.println();
   Serial.println();
   SetupOLED();
   SPrintln("");
}



void SPrint(const char* str) {
  if (DEBUG) {
      Serial.print(str);
  }
  if (OLED) {
      OLEDPrint(str);
  }
}

void SPrint(int value) {
  if (DEBUG) {
    Serial.print(value);
  }
  if (OLED) {
    OLEDPrint(value);
  }  
}

void SPrint(String value) {
  if (DEBUG) {
    Serial.print(value);
  }
  if (OLED) {
    OLEDPrint(value);
  }  
}
void SPrintln(const char* str) {
  if (DEBUG) {
    Serial.println(str);
  }
  if (OLED) {
    OLEDPrintln(str);
  }
}

void SPrintln(int value) {
  if (DEBUG) {
    Serial.println(value);
  }
  if (OLED) {
    OLEDPrintln(value);
  }
}

void blinkRedLED() {
    //pin 0 is reverse wired
   digitalWrite(redLed, HIGH);
   delay(250);
   digitalWrite(redLed, LOW);
   delay(1000);
   digitalWrite(redLed, HIGH);
   
}

int FlipValue(int value) {
  if (value == HIGH)
    return LOW;
  else
    return HIGH;
}
