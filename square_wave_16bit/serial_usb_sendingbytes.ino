#define FOUR_SEC    4000

unsigned long current_time = 0;
unsigned long time_elapsed = 0;
float fmodded_value = 0;
uint16_t j_OCR = 100;
uint16_t j_OCR_old = 100;

void update_timer(uint16_t ocr_val_new){
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
  Serial.begin(9600);
  for(int i=2;i<=13;i++) {
    pinMode(i,OUTPUT); //16bit pin is 9.
  }
  setup_TCC();

}
void loop() {
  //time_elapsed = millis();
  
  if(abs(j_OCR_old-j_OCR) > 0.1) {
    j_OCR_old = j_OCR;
    update_timer(j_OCR_old);
    delay(1000);
    }
    while (Serial.available() == 0) {}
      float value = Serial.parseFloat();
      if(value != 0){ 
        fmodded_value = fmod(value, 8000);
        j_OCR = 16000/(2*(fmodded_value)) - 1;
      }

}

