
#define PIN_CURR A0
#define PIN_CURR_ALARM 12
#define PIN_TEMP_ALARM 11
#define PIN_TEMP A1
#define PIN_STOP_ALARM 10
#define PIN_ACTIVATE 7
#define PIN_HEAT_REQUEST 8


//Square wave on pin 9


#define FOUR_SEC    4000

unsigned long current_time = 0;
unsigned long time_elapsed = 0;
float fmodded_value = 0;
uint16_t j_OCR = 200;

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
}


void handleSerial(){


  if (Serial.available() > 0) {
    float value = Serial.parseFloat();
    if(value != 0){ 
      fmodded_value = fmod(value, 80);
      j_OCR = 16000/(2*(fmodded_value)) - 1;
      update_timer(j_OCR);

    }
  }

}

void loop() {
  handleSerial();

  Serial.print("current:");
  Serial.println(analogRead(PIN_CURR));


  Serial.print("current_alarm:");
  Serial.println(digitalRead(PIN_CURR_ALARM));


  Serial.print("temp:");
  Serial.println(analogRead(PIN_TEMP));


  Serial.print("temp_alarm:");
  Serial.println(digitalRead(PIN_TEMP_ALARM));
  

  Serial.print("manual_alarm:");
  Serial.println(digitalRead(PIN_STOP_ALARM));
  
  
  Serial.print("heat_request:");
  Serial.println(digitalRead(PIN_HEAT_REQUEST));

  digitalWrite(PIN_ACTIVATE, digitalRead(PIN_HEAT_REQUEST));
  
  delay(500);

}

