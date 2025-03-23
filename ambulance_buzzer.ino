int buzzer = 9;

void setup() {
    pinMode(buzzer, OUTPUT);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readString();
        
        if (command == "ON\n") {
            digitalWrite(buzzer, HIGH);
        }
        else if (command == "OFF\n") {
            digitalWrite(buzzer, LOW);
        }
    }
}
