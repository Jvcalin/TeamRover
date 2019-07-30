//Includes


//Private Variables
#define trigPin 15
#define echoPin 13
#define opSensorPin A0

long duration, inches, cm;

void SetupSensors() {
    //SPrint("Starting");
    Serial.println("Start Program");
    pinMode(trigPin, OUTPUT);
    pinMode(opSensorPin, INPUT);
    pinMode(echoPin, INPUT);
}

//Public Functions
bool OpSensorDetect() {
  int reading = analogRead(opSensorPin);
  float proximityV = (float)reading * 5.0 / 1023.0;
  //if (digitalRead(echoPin) == HIGH) {
  if (reading > 60) {
    Serial.println(reading);
    //Serial.println("op!");
    return true;
  }
  else {
    Serial.println(reading);
    return false;
  }
}

void ultrasonicSensorDetect() {
  duration = 0;
  inches = 0;
  cm = 0;

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  //pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH);

  cm = (duration/2) / 29.1;     // Divide by 29.1 or multiply by 0.0343
  inches = (duration/2) / 74;   // Divide by 74 or multiply by 0.0135
  
  Serial.print(duration);
  Serial.print("  --   ");
  Serial.print(inches);
  Serial.print("in,   ");
  Serial.print(cm);
  Serial.print("cm");
  Serial.println();
  
  delay(250);
}



//Private Functions
