#include <HX711.h>
#include <Servo.h> // for controlling the propeller speed.

// Distance sensor pins.
const int DIST_TRIG_PIN = 12;
const int DIST_ECHO_PIN = 13;

// Electric speed controller pins.
const int ESC_PIN = A0; 

// Load cell pins.
const int LOAD_SCK_PINS[] = {10, 8, 6, 4};
const int LOAD_DT_PINS[] = {11, 9, 7, 5};

// Constants for each load cell. Code is 0-indexed, the writing on the load cells is 1-indexed.
const int LOAD_SCALES[] = {-399, -399, -403, -407};

// Initializing load cells.
HX711 loadCells[] = {
  HX711(LOAD_DT_PINS[0], LOAD_SCK_PINS[0]),
  HX711(LOAD_DT_PINS[1], LOAD_SCK_PINS[1]),
  HX711(LOAD_DT_PINS[2], LOAD_SCK_PINS[2]),
  HX711(LOAD_DT_PINS[3], LOAD_SCK_PINS[3])
};


Servo motor;

void setup() {
  Serial.begin(9600);

  // Load cells set pinModes in their constructor.
  pinMode(DIST_TRIG_PIN, OUTPUT);
  pinMode(DIST_ECHO_PIN, INPUT);


  pinMode(ESC_PIN, OUTPUT);


  motor.attach(ESC_PIN);
  Serial.begin(9600);

  for(int i=0; i<4; i++){
    loadCells[i].tare();
    loadCells[i].set_scale(LOAD_SCALES[i]);
  }

  digitalWrite(DIST_TRIG_PIN, LOW);
}

void loop() {
  
  int speed = Serial.parseInt();
  motor.write(speed);

  // Getting data from the distance sensor.
  delayMicroseconds(2);
  digitalWrite(DIST_TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(DIST_TRIG_PIN, LOW);
  const unsigned long duration= pulseIn(DIST_ECHO_PIN, HIGH); // tid mellom sendingen og mottaket i μs.
  int dist = ((duration/2) * 0.343) - 2; // delt på 2 siden signalet reiser frem og tilbake. ganger med lydens hastighet (343 m/s) konvertert til millimetermål. -2 er konstant feil.
  
  int loads[4];
  for(int i=0; i<4; i++){
    loads[i] = loadCells[i].get_units(); // Weight in grams.
  }

  String data = String(dist) + " ";
  for(int i=0; i<4; i++){
    data += String(loads[i]) + " ";
  }
  Serial.println(data);

}
