//Includes
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

//Private Variables
Adafruit_SSD1306 display = Adafruit_SSD1306(128, 32, &Wire);

#if defined(ESP8266)
  #define BUTTON_A  0
  #define BUTTON_B 16
  #define BUTTON_C  2
#elif defined(ESP32)
  #define BUTTON_A 15
  #define BUTTON_B 32
  #define BUTTON_C 14
#endif

String currentLine = "";
String row0 = "";
String row1 = "";
String row2 = "";
String row3 = "";

//Public Functions
void SetupOLED() {
   delay(100);
   // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
   display.begin(SSD1306_SWITCHCAPVCC, 0x3C); // Address 0x3C for 128x32

   display.display();
   delay(1000);
 
   // Clear the buffer.
   display.clearDisplay();
   display.display();

   display.setTextSize(1);
   display.setTextColor(WHITE);
   display.setCursor(0,0);
  
   pinMode(BUTTON_A, INPUT_PULLUP);
   //pinMode(BUTTON_B, INPUT_PULLUP);
   pinMode(BUTTON_C, INPUT_PULLUP);
   
   SPrintln("Starting OLED");

}

void OLEDTick() {
  //Checks to see if the buttons have been pressed
   if(!digitalRead(BUTTON_A)) DoButtonA();
   //if(!digitalRead(BUTTON_B)) DoButtonB();
   if(!digitalRead(BUTTON_C)) DoButtonC();
   
}

void ClearOLED() {
   display.clearDisplay();
   display.display();
   display.setTextSize(1);
   display.setTextColor(WHITE);
   display.setCursor(0,0);
}

void OLEDPrint(char* str) {
   currentLine = currentLine + str;
}

void OLEDPrint(int value) {
   currentLine = currentLine + value;
}

void OLEDPrintln(char* str) {
   currentLine = currentLine + str;
   PushDisplay(currentLine);
}

void OLEDPrintln(int value) {
   String str = String(value);
   currentLine = currentLine + str;
   PushDisplay(currentLine);
}

//Private Functions
void DoButtonA() {
  SPrintln("Button A Pressed");
}

void DoButtonB() {
  SPrintln("Button B Pressed");
}

void DoButtonC() {
  SPrintln("Button C Pressed");
}

void PushDisplay(String nextLine) {
  row0 = row1;
  row1 = row2;
  row2 = row3;
  row3 = nextLine;
  display.clearDisplay();
  display.setCursor(0,0);
  display.println(row0);
  display.println(row1);
  display.println(row2);
  display.println(row3);
  display.display();
  currentLine = "";
}
