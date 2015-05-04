#define XYPAD_X 8
#define XYPAD_Y 9
#include <Servo.h>

Servo R_INA;
Servo R_INB;
Servo L_INA;
Servo L_INB;

void setup() 
{
  Serial.begin(57600);
 
  Serial.setTimeout(5);
  R_INA.attach(0, 20, 90); 
  R_INB.attach(1, 20, 90);
  L_INA.attach(2, 20, 90); 
  L_INB.attach(3, 20, 90); 
}

static uint8_t x_val;
static uint8_t y_val;
double r_throttle = 0;
double l_throttle =0; 

void loop() {
  char buffer[64];
  size_t length = 64; 
      
  length = Serial.readBytes(buffer, length);    
  
  if ( length > 0 )
  { 
    for (int i = 0; i < length - 1; i += 2 )
    {
      if ( buffer[i] == XYPAD_X )
      {
        x_val = buffer[i+1];
      }
      else if ( buffer[i] == XYPAD_Y )
      {
        y_val = buffer[i+1];
      } 
    }
  } 
    
    r_throttle = x_val-128;
    l_throttle = y_val-128;
    
    if (r_throttle <0 && l_throttle<0){
        R_INB.write(-r_throttle);
        L_INB.write(-l_throttle);
    }
    else if (r_throttle <0 && l_throttle>0){
        R_INB.write(-r_throttle);
        L_INA.write(l_throttle);
    }
    else if (r_throttle >0 && l_throttle<0){
        R_INA.write(r_throttle);
        L_INB.write(-l_throttle);
    }
    else
    {R_INA.write(r_throttle);
        L_INA.write(l_throttle);
    }
  
    Bean.setLed( 0, x_val, 0 ); 
    delay(15);
}
