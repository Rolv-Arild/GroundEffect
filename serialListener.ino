const int ESC_PIN = A0; // Electric speed controller
const int DIST_SENSOR_PIN = A1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(ESC_PIN, OUTPUT);
  pinMode(DIST_SENSOR_PIN, INPUT);
}

void loop() {
  String s = Serial.readString();
  if(s == "on"){
    //digitalWrite(2, HIGH);
  }
  else if(s == "off"){
    //digitalWrite(2, LOW);
  }
  int test = analogRead(A1);
  Serial.println(test, BIN);
  delay(2000);
}
