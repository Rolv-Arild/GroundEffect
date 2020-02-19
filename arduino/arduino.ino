#include <HX711.h>

const int ESC_PIN = A1; // Electric speed controller
const int DIST_TRIG_PIN = 12;
const int DIST_ECHO_PIN = 13;
const int LOAD_SCK_PIN = 8;
const int LOAD_DT_PIN = 9;
const int LOAD_SCALE = -399;

HX711 scale(LOAD_DT_PIN, LOAD_SCK_PIN);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(ESC_PIN, OUTPUT);
  pinMode(DIST_TRIG_PIN, OUTPUT);
  pinMode(DIST_ECHO_PIN, INPUT);

  scale.tare();
  scale.set_scale(LOAD_SCALE);
  long zeroFactor = scale.read_average(); // todo: minus dette istedenfor å bruke tare. sparer tid.

  digitalWrite(DIST_TRIG_PIN, LOW);
}

void loop() {
  
  String s = Serial.readString();
  if(s == "on"){
    //digitalWrite(2, HIGH);
  }
  
  delayMicroseconds(2);
  digitalWrite(DIST_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(DIST_TRIG_PIN, LOW);

  const unsigned long duration= pulseIn(DIST_ECHO_PIN, HIGH); // tid mellom sendingen og mottaket i μs.
  int dist = ((duration/2) * 0.343) - 2; // delt på 2 siden signalet reiser frem og tilbake. ganger med lydens hastighet (343 m/s) konvertert til millimetermål. -2 er konstant feil.

  long load = scale.get_units();
  Serial.println(load);

}
