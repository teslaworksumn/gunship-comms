/* This teensy controlls the thrust, rudders, and also returns a low-voltage
 * warning to the BB.
 * Data format: { thrust[0-255], rudder[0-255], lift[0-255],
 *                turret_t[0-255], turret_p[0-255],
 *                fire0[0/37], fire1[0/97], fire2[0/123], 
 *                firectl[0,19,43,59,79]}
 *  
 *  [0-255] means value is between 0 and 255 inclusive
 *  [0/1/2] means that the value is 0 or 1 or 2
 *  
 *  To fire the turret, all three safetys must be high
 *  To move the turret, fire0 must be high
 *  FireCTL dictates which turret is to be fired:
 *   - 00: none
 *   - 19: Turret 1
 *   - 43: Turret 2
 *   - 59: Turret 3
 *   - 79: FIRE ALL!
 *  
 * PINS:
 *   Lift: A14 (DAC)
 *   Turret theta:  3 (PWM)
 *   Turret phi:    4 (PWM)
 *   Turret 1 fire: 23
 *   Turret 2 fire: 22
 *   Turret 3 fire: 21
 */

#define DATA_SIZE 9
#define LIFT_PIN A14
#define TURRET_THETA_PIN 3
#define TURRET_PHI_PIN 4
#define TURRET_FIRE_PIN1 23
#define TURRET_FIRE_PIN2 22
#define TURRET_FIRE_PIN3 21
#define TURRET_FIRE_DELAY 50 // How long to keep the valve open
#define LED_PIN 13

int data[] = {127,127,0,127,127,0,0,0,0};
bool fire[] = {false, false, false};
int clock,clk_offset;

void setup() {
  Serial2.begin(115200);
  analogWriteResolution(8);
  pinMode(LIFT_PIN, OUTPUT);
  pinMode(TURRET_THETA_PIN, OUTPUT);
  pinMode(TURRET_PHI_PIN, OUTPUT);
  pinMode(TURRET_FIRE_PIN1, OUTPUT);
  pinMode(TURRET_FIRE_PIN2, OUTPUT);
  pinMode(TURRET_FIRE_PIN3, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  clock = millis() - clk_offset;
  if (Serial2.available() > 0) {
    if (Serial2.read() == 'x') {
      for (int i=0; i<DATA_SIZE; i++) {
        if (Serial2.available() > 0) {
          data[i] = Serial2.parseInt();
        } else {
          break;
        }
      }
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
  
  analogWrite(LIFT_PIN, data[2]);
  if (fire[0]) {
    analogWrite(TURRET_THETA_PIN, data[3]);
    analogWrite(TURRET_PHI_PIN, data[4]);
  }
  if (fire[0] && fire[1] && fire[2]) {
    switch (data[8]) {
      case 19:
        digitalWrite(TURRET_FIRE_PIN1, HIGH);
        digitalWrite(TURRET_FIRE_PIN2, LOW);
        digitalWrite(TURRET_FIRE_PIN3, LOW);
        break;
      case 43:
        digitalWrite(TURRET_FIRE_PIN1, LOW);
        digitalWrite(TURRET_FIRE_PIN2, HIGH);
        digitalWrite(TURRET_FIRE_PIN3, LOW);
        break;
      case 59:
        digitalWrite(TURRET_FIRE_PIN1, LOW);
        digitalWrite(TURRET_FIRE_PIN2, LOW);
        digitalWrite(TURRET_FIRE_PIN3, HIGH);
        break;
      case 79:
        digitalWrite(TURRET_FIRE_PIN1, HIGH);
        digitalWrite(TURRET_FIRE_PIN2, HIGH);
        digitalWrite(TURRET_FIRE_PIN3, HIGH);
        break;
      default:
        digitalWrite(TURRET_FIRE_PIN1, LOW);
        digitalWrite(TURRET_FIRE_PIN2, LOW);
        digitalWrite(TURRET_FIRE_PIN3, LOW);
        break;
    }
  } else {
    digitalWrite(TURRET_FIRE_PIN1, LOW);
    digitalWrite(TURRET_FIRE_PIN2, LOW);
    digitalWrite(TURRET_FIRE_PIN3, LOW);
  }
}

void rclock() {
  clk_offset = millis();
}
  
