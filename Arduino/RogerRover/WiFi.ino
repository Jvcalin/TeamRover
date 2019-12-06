#include "ESP8266WiFi.h"
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"
#include <aREST.h>

#define MQTT_SERVER      "192.168.1.39"
#define MQTT_SERVERPORT  1883
#define AIO_USERNAME    "jvcalin"
#define AIO_KEY         "xxxxxxxxxx"


aREST rest = aREST();

const char* ssid = "Daenerys";
const char* password = "jonandpaul";

// Store the MQTT server, username, and password in flash memory.
// This is required for using the Adafruit MQTT library.
const char MQTT_SERVER[] PROGMEM    = MQTT_SERVER;
const char MQTT_USERNAME[] PROGMEM  = AIO_USERNAME;
const char MQTT_PASSWORD[] PROGMEM  = AIO_KEY;


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
