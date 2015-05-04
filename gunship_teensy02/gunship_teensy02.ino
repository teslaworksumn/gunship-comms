/* This teensy controlls the lift and turret
 * Data format: { thrust[0-255], rudder[0-255], lift[0-255],
 *                turret_t[0-255], turret_p[0-255],
 *                fire0[0/37], fire1[0/97], fire2[0/123] }
 *  
 *  [0-255] means value is between 0 and 255 inclusive
 *  [0/1/2] means that the value is 0 or 1 or 2
 *  
 *  To fire the turret, all three safetys must be high
 *  To move the turret, fire0 must be high
 *  
 * PINS:
 *   Lift: A14 (DAC)
 *   Turret theta: 3 (PWM)
 *   Turret phi:   4 (PWM)
 *   Turret fire:  5
 */

#define DATA_SIZE 8
#define LIFT_PIN A14
#define TURRET_THETA_PIN 3
#define TURRET_PHI_PIN 4
#define TURRET_FIRE_PIN 5
#define TURRET_FIRE_DELAY 50 // How long to keep the valve open
#define LED_PIN 13

int data[] = {127,127,0,127,127,0,0,0};
bool fire[] = {false, false, false};

void setup() {
  Serial2.begin(115200);
  analogWriteResolution(8);
  pinMode(LIFT_PIN, OUTPUT);
  pinMode(TURRET_THETA_PIN, OUTPUT);
  pinMode(TURRET_PHI_PIN, OUTPUT);
  pinMode(TURRET_FIRE_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  if (Serial2.available() > 0) {
    if (Serial2.read() == 'x') {
      for (int i=0; i<DATA_SIZE; i++) {
        if (Serial2.available() > 0) {
          data[i] = Serial2.parseInt();
        } else {
          break;
        }
      }
      digitalWrite(LED_PIN, HIGH);
      delay(25);
      digitalWrite(LED_PIN, LOW);
      delay(25);
    }
  }
  if (data[5] == 37) {
    fire[0] = true;
  } else {
    fire[0] = false;
  }
  if (data[6] == 97) {
    fire[1] = true;
  } else {
    fire[1] = false;
  }
  if (data[7] == 123) {
    fire[3] = true;
  } else {
    fire[3] = false;
  }
  
  analogWrite(A14, data[2]);
  if (fire[0]) {
    analogWrite(TURRET_THETA_PIN, data[3]);
    analogWrite(TURRET_PHI_PIN, data[4]);
  }
  if (fire[0] && fire[1] && fire[2]) {
    digitalWrite(TURRET_FIRE_PIN, HIGH);
    delay(TURRET_FIRE_DELAY); // Keep the valve open for x of milliseconds
    digitalWrite(TURRET_FIRE_PIN, LOW);
    
  } else {
    digitalWrite(TURRET_FIRE_PIN,LOW);
  }
}
  
