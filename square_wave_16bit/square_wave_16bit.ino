
//Square wave on pin 11


volatile uint16_t val=80;


void callme()
{
  Serial.println("here3");
  delay(1000);
  Serial.println((unsigned int)TCCR2A);
  Serial.println("here4");
  Serial.println((unsigned int)TCCR2B);
  Serial.println("here5");
  
  delay(1000);
  noInterrupts();
  TCCR1A = ( 1<<COM1A0 );
  TCCR1B = (1<<WGM12 | 1<<CS10); //CTC | Timer1 Register, CS10 (Noprescaler clk/1)

  update_timer();
  interrupts();
}

void update_timer(){
  OCR1A = 450;  // Freq = fclk/(2*prescale*(1+OCR1A))
}


void setup() {
  // put your setup code here, to run once:
  for(int i=2;i<=13;i++){
    pinMode(i,OUTPUT); //16bit pin is 9.
  }

  Serial.begin(9600);
  Serial.println("hello world!");

  delay(1000);

  callme(); // timer initialize

  Serial.println("Hi");
}

void loop() {
  update_timer();
  delay(1000);
  return;

 /* for(uint8_t i =10;i<200;i++){

    val=i;
    update_timer();
    delay(100);
  }
*/

}
