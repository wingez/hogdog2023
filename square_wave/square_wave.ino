
//Square wave on pin 11


volatile uint8_t val=25;


void callme()
{
// WGM0[1:0]= 10, for CTC mode
// COM0[1:0]= 01, to toggle OC0 on compare match
// CS0[2:0] =010. for prescaler 8
  Serial.println("here3");
  delay(1000);
  Serial.println((unsigned int)TCCR2A);
  Serial.println("here4");
  Serial.println((unsigned int)TCCR2B);
  Serial.println("here5");
  
  delay(1000);
  noInterrupts();
  TCCR2A = (1<<WGM21 | 1<<COM2A0 );
  TCCR2B = (1<<CS21);
  //TCCR0A=(1<<WGM01)|(1<<COM0A0)|(1<<CS01);
  //TIMSK2=(1<<OCIE2A); //enable output compare interrupt 
  Serial.println("here");
  OCR2A = val;
  Serial.println("here2");
  interrupts();
}

void update_timer(){
  OCR2A = val;
}

ISR(TIMER2_COMP_vect) // interrupt subroutine
{
  OCR2A=(uint8_t)val; //put OCR value
}


void setup() {
  // put your setup code here, to run once:
  for(int i=2;i<=13;i++){
    pinMode(i,OUTPUT);
  }

  Serial.begin(9600);
  Serial.println("hello world!");

  delay(1000);
  //val=9;
  Serial.println("H2");
  callme(); // timer initialize
  //interrupts(); // enable global interrupts
  Serial.println("Hi");
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("here6");
  val=38;
  update_timer();
  delay(1000);
  return;
  for(uint8_t i =10;i<200;i++){

    val=i;
    update_timer();
    delay(100);
  }


}
