
int ButtonPin = 48;
int ButtonPin2 = 11;
int lastX = 0;
int lastY = 0;
int lastIquals = 0;
void setup() {
 // put your setup code here, to run once:
 pinMode(ButtonPin, INPUT);
 pinMode(ButtonPin2,INPUT);
 Serial.begin(9600);
}

void loop() {
 // put your main code here, to run repeatedly:
 int x = digitalRead(ButtonPin);
 int y = digitalRead(ButtonPin2);
 if (x == HIGH && lastX == 0) {
  Serial.println('1');
  lastX = 1;
 }
 else{
  if(x == LOW){
    lastX = 0;
  }
 }
 
 if(y == HIGH && lastY == 0){
   Serial.print('2');
   lastY = 1;
 }
 else{
  if(y == LOW){
    lastY = 0;
  }
 }

 if(x != y){
  lastIquals = 0;
 }
 
 else{
  /*if(lastIquals == 0){
    Serial.println('0');
    lastIquals = 1;}*/
    Serial.print('0');
    
  
 }
 delay(200);
