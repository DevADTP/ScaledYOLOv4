#include  <M5Atom.h>

#define TRIG 23
#define DLED 33

String command;

void setup() {
  M5.begin(false, false, true);
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, 22, 19);
 // M5.dis.drawpix(0, 0x00f000);
  pinMode(TRIG, OUTPUT);
  pinMode(DLED, INPUT);
  digitalWrite(TRIG, HIGH);
}

void loop() {
  if(Serial.available()){
    command = Serial.readStringUntil('\n');
    if(command.equals("1")){
      M5.dis.drawpix(0, 0xf00000); // turn on green
    }
    else if(command.equals("0")){
      M5.dis.drawpix(0, 0x00f000); //turn on red
    }
  }
  
  if(digitalRead(39) == LOW){
    digitalWrite(TRIG, LOW);
  }else {
    digitalWrite(TRIG, HIGH);
  }
  if(digitalRead(DLED) == HIGH){
    while(Serial2.available() > 0){
      char ch = Serial2.read();
      Serial.print(ch);
    }
  }
  delay(10);
  M5.update();
}
