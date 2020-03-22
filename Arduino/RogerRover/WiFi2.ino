//https://github.com/plapointe6/EspMQTTClient

#include "EspMQTTClient.h"

#define BEEP_FEED "roger/cmd/feather/beep"
#define MOTOR_FEED "roger/cmd/feather/motor"
#define SERVO_FEED "roger/cmd/feather/servo"
#define BASE_TOPIC_PATH "roger/sensors/feather/"


EspMQTTClient client(
  "Daenerys",
  "jonandpaul",
  "192.168.1.25",  // MQTT Broker server ip
  "",
  "",
  "RogerFeather",      // Client name that uniquely identify your device
  1883
);

void onConnectionEstablished() {

  client.subscribe(BEEP_FEED, [] (const String &payload)  {
    beepMessage(payload);
    SPrintln(payload);
  });

  client.subscribe(MOTOR_FEED, [] (const String &payload)  {
    motorMessage(payload);
    SPrintln(payload);
  });

  //client.subscribe(SERVO_FEED, [] (const String &payload)  {
  //  servoMessage(payload);
  //  SPrintln(payload);
  //});

  client.publish("roger/status/feather", "Feather coming online");
}

void WiFiTick() {
  client.loop();
}

void beepMessage(String message) {
  Play(message);
}

void motorMessage(String message) {
  SetCurrentAction(message);
}

void servoMessage(String message) {
  
}

void MQTTPublishStatus(String statusmsg) {
  
  SPrintln("About to publish");
  MQTTPublish("roger/status/feather", statusmsg);

}

void MQTTPublish(const char* topic, char* message) {
  SPrintln(topic);
  SPrintln(message);
  SPrintln("Publishing!");
  client.publish(topic, message);
}

void MQTTPublish(String topic, String message) {
  SPrintln(topic);
  SPrintln(message);
  SPrintln("Publishing!");
  client.publish(topic, message);
}

void MQTTPublishSensors() {
  MQTTPublish(BASE_TOPIC_PATH "proxf", String(getFrontDistance()));
  MQTTPublish(BASE_TOPIC_PATH "proxb", String(getBackDistance()));
  MQTTPublish(BASE_TOPIC_PATH "proxl", String(getLeftDistance()));
  MQTTPublish(BASE_TOPIC_PATH "proxr", String(getRightDistance()));
  MQTTPublish(BASE_TOPIC_PATH "motorspeed", String(getCurrSpeed()));
  MQTTPublish(BASE_TOPIC_PATH "motoraction", String(getCurrentAction()));
  MQTTPublish(BASE_TOPIC_PATH "servohpos", String(getServoHPos()));
  MQTTPublish(BASE_TOPIC_PATH "servovpos", String(getServoVPos()));
}
