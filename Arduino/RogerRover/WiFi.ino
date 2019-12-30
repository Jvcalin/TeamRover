#include "ESP8266WiFi.h"
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"
#include <aREST.h>



//Topics
//roger/status
//roger/status/feather
//roger/status/matrix

//roger/cmd/feather/beep => "swoopup"
//roger/cmd/feather/motor => "forward"
//roger/cmd/feather/servo => "h,v"
//roger/sensors/feather/proxf
//roger/sensors/feather/proxb
//roger/sensors/feather/proxl
//roger/sensors/feather/proxr
//roger/sensors/feather/motor/speed
//roger/sensors/feather/motor/action
//roger/sensors/feather/servo/h
//roger/sensors/feather/servo/v
//roger/sensors/feather/bump
//roger/sensors/feather/vib
//roger/sensors/feather/charging
//roger/sensors/feather/batt
//roger/sensors/feather/power

#define MQTT_SERVER      "192.168.1.25"
#define MQTT_SERVERPORT  1883
#define AIO_USERNAME    "jvcalin"
#define AIO_KEY         "xxxxxxxxxx"

// Store the MQTT server, username, and password in flash memory.
// This is required for using the Adafruit MQTT library.
//const char MQTT_SERVER[] PROGMEM    = MQTT_SERVER;
//const char MQTT_USERNAME[] PROGMEM  = AIO_USERNAME;
//const char MQTT_PASSWORD[] PROGMEM  = AIO_KEY;

// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, MQTT_SERVER, MQTT_SERVERPORT, AIO_USERNAME, AIO_KEY);

const char BEEP_FEED[] PROGMEM = "roger/cmd/feather/beep";
const char MOTOR_FEED[] PROGMEM = "roger/cmd/feather/beep";
const char SERVO_FEED[] PROGMEM = "roger/cmd/feather/beep";

Adafruit_MQTT_Subscribe beepCmd = Adafruit_MQTT_Subscribe(&mqtt, BEEP_FEED);
Adafruit_MQTT_Subscribe motorCmd = Adafruit_MQTT_Subscribe(&mqtt, MOTOR_FEED);
Adafruit_MQTT_Subscribe servoCmd = Adafruit_MQTT_Subscribe(&mqtt, SERVO_FEED);

aREST rest = aREST();

const char* ssid = "Daenerys";
const char* password = "jonandpaul";



// The port to listen for incoming TCP connections 
#define LISTEN_PORT           80

// Create an instance of the server
//WiFiServer server(LISTEN_PORT);

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
  //server.begin();
  //SPrintln("Server started");
  
  // Print the IP address
  //SPrintln(WiFi.localIP());

  mqtt.subscribe(&beepCmd);
  mqtt.subscribe(&motorCmd);
  mqtt.subscribe(&servoCmd);

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
  //WiFiClient client = server.available();
  //if (!client) {
  //  return;
  //}
  //while(!client.available()){
  //  delay(1);
  //}
  //rest.handle(client);

  // Ensure the connection to the MQTT server is alive (this will make the first
  // connection and automatically reconnect when disconnected).  See the MQTT_connect
  // function definition further below.
  MQTT_connect();


  //Read Subscriptions
  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription(100))) {
    if (subscription == &beepCmd) {
      Serial.print(F("Got: "));
      Serial.println((char *)beepCmd.lastread);
    }
    if (subscription == &motorCmd) {
      Serial.print(F("Got: "));
      Serial.println((char *)motorCmd.lastread);
    }
    if (subscription == &servoCmd) {
      Serial.print(F("Got: "));
      Serial.println((char *)servoCmd.lastread);
    }
  }
}


// Function to connect and reconnect as necessary to the MQTT server.
// Should be called in the loop function and it will take care if connecting.
void MQTT_connect() {
  int8_t ret;

  // Stop if already connected.
  if (mqtt.connected()) {
    return;
  }

  //Attempt to connect and abandon on fail
  SPrintln("Connecting to MQTT... ");
  if ((ret = mqtt.connect()) != 0) {  // connect will return 0 for connected
    SPrintln("Could not connect to MQTT.");
    SPrintln((int)mqtt.connectErrorString(ret));
    mqtt.disconnect();
  }
  else
    Serial.println("MQTT Connected!");
}
