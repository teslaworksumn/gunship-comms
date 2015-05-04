/* This teensy controlls the thrust, rudders, and also returns a low-voltage
 * warning to the BB.
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
 *   Thrust: A14 (DAC)
 *   Rudders: 6 (PWM)
 *   Low-Voltage warning (input): 15 (A1) (HIGH means voltage OK)
 */

#define DATA_SIZE 8
#define THRUST_PIN A14
#define RUDDER_PIN 6
#define LVW_PIN 15
#define LED_PIN 13

int data[] = {127,127,0,127,127,0,0,0};

void setup() {
  Serial2.begin(115200);
  analogWriteResolution(8);
  pinMode(THRUST_PIN, OUTPUT);
  pinMode(RUDDER_PIN, OUTPUT);
  pinMode(LVW_PIN, INPUT);
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
      digitalWrite(LED_PIN,HIGH);
      delay(25);
      digitalWrite(LED_PIN,LOW);
      delay(25);
    }
  }
  
  analogWrite(THRUST_PIN, data[0]);
  analogWrite(RUDDER_PIN, data[1]);
  
  Serial2.write('x');
  Serial2.write(' ');
  if (digitalRead(LVW_PIN) == HIGH) {
    Serial2.print('0');
    digitalWrite(LED_PIN,LOW);
  } else {
    Serial2.print('1');
    digitalWrite(LED_PIN,HIGH);
  }
  Serial2.write('\c');
  Serial2.write('\n');
}
  
