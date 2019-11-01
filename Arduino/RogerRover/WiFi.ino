#include "ESP8266WiFi.h"
#include <aREST.h>


aREST rest = aREST();

const char* ssid = "wifi-name";
const char* password = "wifi-pass";

// The port to listen for incoming TCP connections 
#define LISTEN_PORT           80

// Create an instance of the server
WiFiServer server(LISTEN_PORT);

//Public Functions
void SetupWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    SPrint(".");
  }
  SPrintln("");
  SPrintln("WiFi connected");
 
  // Start the server
  server.begin();
  SPrintln("Server started");
  
// Print the IP address
  SPrintln(WiFi.localIP());
}

void AddWiFiFunctions() {
  //rest.function("ServoMoveRight", ServoMoveRight);
  //rest.function("ServoMoveLeft", ServoMoveLeft);
  //rest.function("ServoMoveUp", ServoMoveUp);
  //rest.function("ServoMoveDown", ServoMoveDown);
  //rest.function("ResetServos", ResetServos);

  //Function must return an int and accept a String as a parameter
  //TODO:  Write wrapper functions on all functions you want to make public
}

void WiFiTick() {
  // Handle REST calls
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
  while(!client.available()){
    delay(1);
  }
  rest.handle(client);
}
