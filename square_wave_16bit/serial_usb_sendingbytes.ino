float send_value = 3.14159;

void setup() {
  Serial.begin(9600);
}
void loop() {
  while(Serial.available() == 0 ){}
  float value = Serial.parseFloat();
  value *= 2;
  delay(10);
  Serial.println(value);
  }
