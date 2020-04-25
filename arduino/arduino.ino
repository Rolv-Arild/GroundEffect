#include <HX711.h>
#include <Servo.h> // for controlling the propeller speed.

// Distance sensor pins.
const int DIST_TRIG_PIN = 12;
const int DIST_ECHO_PIN = 13;

// Electric speed controller pins.
const int ESC_PINS[] = {A0, A1, A2, A3};
const int MOTOR_THRESHOLDS[] = {70, 94, 64, 107};

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

Servo motors[] = {
  Servo(),
  Servo(),
  Servo(),
  Servo()  
};


void setup() {
  Serial.begin(9600);

  // Load cells set pinModes in their constructor.
  pinMode(DIST_TRIG_PIN, OUTPUT);
  pinMode(DIST_ECHO_PIN, INPUT);

  for(int i=0; i<4; i++){
    pinMode(ESC_PINS[i], OUTPUT);
    motors[i].attach(ESC_PINS[i]);
  }

  for(int i=0; i<4; i++){
    loadCells[i].tare();
    loadCells[i].set_scale(LOAD_SCALES[i]);
  }

  digitalWrite(DIST_TRIG_PIN, LOW);
}

void loop() {
  String in = Serial.readString();
  int speeds[] = {20, 20, 20, 20};
  int speedIndex = 0;
  String s = "";
  for(int i=0; i<in.length(); i++){
    if(in[i] == ' '){
      speeds[speedIndex] = s.toInt();
      s = "";
      speedIndex++;
    } else{
      s += String(in[i]);
    }
  }

  for(int i=0; i<4; i++){
    // Normalizing speed input (0-70) to each rotors appropriate amount.
    if(speeds[i] == 0){
      speeds[i] = 20;
    } else if(speeds[i] > 70){
      speeds[i] = 180;
    } else{
      speeds[i] = map(speeds[i], 0, 70, MOTOR_THRESHOLDS[i], 180);
    } 
  }

  for(int i=0; i<4; i++){
    motors[i].write(speeds[i]);
  }

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
