#include "ESP8266WiFi.h"
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"
//#include <aREST.h>



//Topics

//PUBLISH
//roger/status
//roger/status/feather
//roger/status/matrix
//roger/sensors/feather/proxf
//roger/sensors/feather/proxb
//roger/sensors/feather/proxl
//roger/sensors/feather/proxr
//roger/sensors/feather/motorspeed
//roger/sensors/feather/motoraction
//roger/sensors/feather/servohpos
//roger/sensors/feather/servovpos
//roger/sensors/feather/bump
//roger/sensors/feather/vib
//roger/sensors/feather/charging
//roger/sensors/feather/batt
//roger/sensors/feather/power

//SUBSCRIBE
//roger/cmd/feather/beep => "swoopup"
//roger/cmd/feather/motor => "forward"
//roger/cmd/feather/servo => "h,v"

#define MQTT_SERVER      "192.168.1.25"
#define MQTT_SERVERPORT  1883
#define AIO_USERNAME    "jvcalin"
#define AIO_KEY         "xxxxxxxxxx"
#define BASE_TOPIC_PATH "roger/sensors/feather/"

// Store the MQTT server, username, and password in flash memory.
// This is required for using the Adafruit MQTT library.
//const char MQTT_SERVER[] PROGMEM    = MQTT_SERVER;
//const char MQTT_USERNAME[] PROGMEM  = AIO_USERNAME;
//const char PHOTOCELL_FEED[] = AIO_USERNAME "/feeds/photocell";
//const char MQTT_PASSWORD[] PROGMEM  = AIO_KEY;

// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, MQTT_SERVER, MQTT_SERVERPORT, AIO_USERNAME, AIO_KEY);

#define BEEP_FEED "roger/cmd/feather/beep"
#define MOTOR_FEED "roger/cmd/feather/motor"
#define SERVO_FEED "roger/cmd/feather/servo"

Adafruit_MQTT_Subscribe beepCmd = Adafruit_MQTT_Subscribe(&mqtt, BEEP_FEED);
//Adafruit_MQTT_Subscribe motorCmd; //= Adafruit_MQTT_Subscribe(&mqtt, MOTOR_FEED);
//Adafruit_MQTT_Subscribe servoCmd; //= Adafruit_MQTT_Subscribe(&mqtt, SERVO_FEED);

//aREST rest = aREST();

const char* ssid = "Daenerys";
const char* password = "jonandpaul";

// Bug workaround for Arduino 1.6.6, it seems to need a function declaration
// for some reason (only affects ESP8266, likely an arduino-builder bug).
void MQTT_connect();

// The port to listen for incoming TCP connections 
#define LISTEN_PORT           80

// Create an instance of the server
//WiFiServer server(LISTEN_PORT);

//Public Functions
void SetupWiFi() {

  //SPrintln(F("Adafruit MQTT demo"));
  
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
  SPrintln(WiFi.localIP());
  //MQTTPublishStatus("Feather powering up");
  mqtt.subscribe(&beepCmd);
  //mqtt.subscribe(&motorCmd);
  //mqtt.subscribe(&servoCmd);

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
  SPrint(".");
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
  while ((subscription = mqtt.readSubscription(5000))) {
    //SPrintln(subscription);
    if (subscription == &beepCmd) {
      Play((char *)beepCmd.lastread);
      SPrint("Got: ");
      SPrintln((char *)beepCmd.lastread);
    }
    //if (subscription == &motorCmd) {
    //  SetCurrentAction((char *)motorCmd.lastread);
    //  Serial.print(F("Got: "));
    //  Serial.println((char *)motorCmd.lastread);
    //}
    //if (subscription == &servoCmd) {
      //Serial.print(F("Got: "));
      //Serial.println((char *)servoCmd.lastread);
    //}
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
  
  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) { // connect will return 0 for connected
       SPrintln((int)(mqtt.connectErrorString(ret)));
       SPrintln("Retrying MQTT connection in 5 seconds...");
       mqtt.disconnect();
       delay(5000);  // wait 5 seconds
       retries--;
       if (retries == 0) {
         // basically die and wait for WDT to reset me
         SPrintln("Can't connect... reset me");
         while (1);
       }
  }
  SPrintln("MQTT Connected!");

}

void MQTTPublishStatus(String statusmsg) {
  MQTT_connect();

  if (mqtt.connected()) {
    MQTTPublish("roger/status/feather",StringToCharArray(statusmsg));
  }
}

void MQTTPublish(const char* topic, char* message) {
  String fulltopic = String(BASE_TOPIC_PATH);
  fulltopic = fulltopic.concat(String(topic));

  Adafruit_MQTT_Publish pub = Adafruit_MQTT_Publish(&mqtt, StringToCharArray(fulltopic));
  pub.publish(message);
  delete &pub;
}

void MQTTPublishSensors() {
  MQTTPublish("proxf", StringToCharArray(String(getFrontDistance())));
  MQTTPublish("proxb", StringToCharArray(String(getBackDistance())));
  MQTTPublish("proxl", StringToCharArray(String(getLeftDistance())));
  MQTTPublish("proxr", StringToCharArray(String(getRightDistance())));
  MQTTPublish("motorspeed", StringToCharArray(String(getCurrSpeed())));
  MQTTPublish("motoraction", StringToCharArray(String(getCurrentAction())));
  MQTTPublish("servohpos", StringToCharArray(String(getServoHPos())));
  MQTTPublish("servovpos", StringToCharArray(String(getServoVPos())));
}

char* StringToCharArray(String str) {
  int bufsize = str.length();
  char buf[bufsize];
  str.toCharArray(buf, bufsize);
  return buf; 
}
