
//Square wave on pin 9

int j = 0;
void callme()
{
  delay(1000);

  delay(1000);
  noInterrupts();
  TCCR1A = ( 1<<COM1A0 );
  TCCR1B = (1<<WGM12 | 1<<CS10 ); //CTC | Timer1 Register, CS10 (Noprescaler clk/1)

  update_timer();
  interrupts();
}

void update_timer(){
  
  OCR1A = 150;  // Freq = fclk/(2*prescale*(1+OCR1A))
}
void update_timer(uint16_t ocr_val_new){
  TCCR1B &= ~(1<<CS10 ); //pause (1x prescaler)

  OCR1A = ocr_val_new;
  if ( TCNT1 >= ocr_val_new){
      TCNT1 = ocr_val_new-4; 
  }
  TCCR1B |= (1<<CS10 ); //resume (1x prescaler)
  return;
}

void setup() {
  // put your setup code here, to run once:
  for(int i=2;i<=13;i++){
    pinMode(i,OUTPUT); //16bit pin is 9.
  }

  Serial.begin(9600);

  delay(1000);

  callme(); 
  OCR1A = 150;
}

void loop() {
  for(uint16_t i =150;i<400;i++){
    update_timer(i); //Updates value in OCR1A
    if (i==150){
      j++;
      if (j > 3) { //Starts a triggerwave on 12 to see if successful wrap
      digitalWrite(12, HIGH);
      delay(2000);
      digitalWrite(12,LOW);

      }
    }
    
    delay(50);
  }
  
  return;


}
