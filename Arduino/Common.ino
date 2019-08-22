//These are common functions used by everyone

#define DEBUG true
#define OLED true

void SetupSerial(){
   Serial.begin(115200);
   SetupOLED();
}



void SPrint(char* str) {
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

void SPrintln(char* str) {
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
