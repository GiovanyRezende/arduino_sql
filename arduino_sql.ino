#include "dht.h"

const int sensor = A0;
dht DHT;
const int foto = A1;
float temp;
float umid;
int lum;

void setup() {
  Serial.begin(9600);
}

void loop() {
  DHT.read11(sensor);
  temp = DHT.temperature;
  umid = DHT.humidity;
  lum = analogRead(foto);

  Serial.print(temp);
  Serial.print(",");
  Serial.print(umid);
  Serial.print(",");
  Serial.println(lum);
  
  delay(1000);
}

