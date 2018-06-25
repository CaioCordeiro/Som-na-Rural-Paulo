
#include <Ultrasonic.h>
#include <LiquidCrystal.h>

int btnEsq = 6, btnDir = 7, LedEsq = 8, ledDir = 9, ledLuz = 10;

Ultrasonic ultrasonic(2,3);
LiquidCrystal lcd (34,32,30,28,26,24);

void setup(){
  pinMode(ledEsq,OUTPUT);
  pinMode(ledDir,OUTPUT);
  pinMode(ledLuz,OUTPUT);
  pinMode(btnEsq,INPUT);
  pinMode(btnDir,INPUT);
  lcd.begin(16,2);
}

void loop(){
  int distance = ultrasonic.distanceRead();

  //LDR - Se estiver ficando escuro = acender faixa de LED na bike
  if(analogRead(A0) < 420)
    digitalWrite(ledLuz, HIGH);
  else 
    digitalWrite(ledLuz, LOW);

  //Pisca-alerta - se apertar bptap direito = ligar pisca-alerta direito
  if(digitalRead(btnDir) == HIGH)
    piscaAlerta(ledDir);
  
  
  lcd.clear();
}

void printDistance(){
  lcd.print("Distancia em CM:")
  lcd.setCursor(1,5);
  lcd.print(distance);
}

void piscaAlerta(int whichLed){
    digitalWrite(whichLed, HIGH);
    delay(250);
    digitalWrite(whichLed,LOW);
}

