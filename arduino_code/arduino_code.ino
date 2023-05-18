
#include "definitions.h"

#define PIN_CURR A0
#define PIN_CURR_ALARM 12
#define PIN_TEMP_ALARM 11
#define PIN_TEMP A1
#define PIN_STOP_ALARM 10
#define PIN_ACTIVATE 7
#define PIN_HEAT_REQUEST 8

const unsigned int current_threshold=350;

unsigned long msLastOvercurrent=0;

const unsigned long backoffDurationMs=15*1000;

unsigned long nextPrintMs = 0;

int isActive=LOW;
//Square wave on pin 9


#define FOUR_SEC    4000

unsigned long current_time = 0;
unsigned long time_elapsed = 0;
float fmodded_value = 0;
uint16_t j_OCR = 200;

float frequency_khz = 35.0;

void update_timer(uint16_t ocr_val_new){

  
  if (ocr_val_new<160){
    ocr_val_new=160;
  }

  TCCR1B &= ~(1<<CS10 ); //pause (1x prescaler)

  OCR1A = ocr_val_new;
  if ( TCNT1 >= ocr_val_new){
      TCNT1 = ocr_val_new-1; 
  }
  TCCR1B |= (1<<CS10 ); //resume (1x prescaler)
  
  Serial.print("Updating frequency, New OCR: ");
  Serial.println(ocr_val_new);
  Serial.print("\n");
  return;
}

void setup_TCC()
{
  noInterrupts();
  TCCR1A = ( 1<<COM1A0 );
  TCCR1B = (1<<WGM12 | 1<<CS10 ); //CTC | Timer1 Register, CS10 (Noprescaler clk/1)
  update_timer(j_OCR);
  interrupts();
}

void setup() {

  pinMode(PIN_CURR_ALARM,INPUT);
  pinMode(PIN_TEMP_ALARM,INPUT);
  pinMode(PIN_STOP_ALARM,INPUT);
  pinMode(PIN_ACTIVATE,OUTPUT);
  pinMode(PIN_HEAT_REQUEST, INPUT);

  pinMode(9,OUTPUT);
  Serial.begin(115200);
  setup_TCC();

  setFrequencyKHz(frequency_khz);
}

void setFrequencyKHz(float value){
    if(value != 0){
      fmodded_value = fmod(value, 80);
      j_OCR = 16000/(2*(fmodded_value)) - 1;
      update_timer(j_OCR);
    }
}


coordinate2d_t coord_array[] =
   {
   {53.32, 120},
   {60.66, 115},
   {69.15, 110},
   {79.00, 105},
   {90.45, 100},
   {103.8 , 95},
   {119.4, 90},
   {137.7 , 85},
   {159.3, 80},
   {184.7, 75},
   {214.9, 70},
   {250.8, 65},
   {293.7, 60},
   {345.2, 55},
   {407.4, 50},
   {482.7, 45},
   {574.6, 40},
   {687.3, 35},
   {826.6, 30},
   {1000, 25},
   {1217, 20},
   {1491, 15},
   {1838, 10},
   {2282, 5},
   {2854, 0},
    };

//Takes coordinate_array, certain x and size of coord_array
float interpolate(coordinate2d_t *coord_array, int n, float x) {
    float x_diff = 0;
    float consec_diff = 0;

    for(int i = 0; i < n-1; i++) { //loops through array
        //checks if requested x val is between 2 cosecutive values
        if (coord_array[i].x <= x && coord_array[i+1].x >= x ) {
            x_diff = x - coord_array[i].x;
            consec_diff = coord_array[i+1].x - coord_array[i].x;
            //returns lowerbound + linear interpolation
            return coord_array[i].y + (coord_array[i+1].y - coord_array[i].y) * x_diff/consec_diff;
        }
    }

    return -1; //neg for illegal interpolation
}


void printTemp(){

    float q = ((float) analogRead(PIN_TEMP)) / 1024.0f;

    float r = 330;

    float n = (q*r)/(1.0f-q);

    float tmp = interpolate(coord_array, sizeof(coord_array)/sizeof(coordinate2d_t), n);



    Serial.print("temp:");
    Serial.println(tmp);



}


void printInfo(){
  Serial.print("current:");
  Serial.println(analogRead(PIN_CURR));


  Serial.print("current_alarm:");
  Serial.println(digitalRead(PIN_CURR_ALARM));

  printTemp();

  Serial.print("temp_alarm:");
  Serial.println(digitalRead(PIN_TEMP_ALARM));


  Serial.print("manual_alarm:");
  Serial.println(digitalRead(PIN_STOP_ALARM));


  Serial.print("heat_request:");
  Serial.println(digitalRead(PIN_HEAT_REQUEST));


  Serial.print("is_active:");
  Serial.println(isActive);


}

void loop() {

  unsigned long currentMs = millis();

  if(nextPrintMs < currentMs ) {
    printInfo();
    nextPrintMs = currentMs+500;
  }


  if(!digitalRead(PIN_HEAT_REQUEST)){
    digitalWrite(PIN_ACTIVATE, LOW);
  } else {

    unsigned int current_sense = analogRead(PIN_CURR);


    if(msLastOvercurrent==0 || currentMs>(msLastOvercurrent + backoffDurationMs)) {
        isActive = HIGH;
    }

    if (current_sense>=current_threshold){
        isActive = LOW;
        msLastOvercurrent = currentMs;
    }

    digitalWrite(PIN_ACTIVATE, isActive);

  }
}
