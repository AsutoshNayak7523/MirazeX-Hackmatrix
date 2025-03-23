#define RED_PIN 7
#define GREEN_PIN 6
#define BUZZER 5

void setup() {
    Serial.begin(9600);
    pinMode(RED_PIN, OUTPUT);
    pinMode(GREEN_PIN, OUTPUT);
    pinMode(BUZZER, OUTPUT);
}

void loop() {
    if (Serial.available() > 0) {
        char received = Serial.read();
        
        if (received == 'G') {
            digitalWrite(GREEN_PIN, HIGH);
            digitalWrite(RED_PIN, LOW);
            digitalWrite(BUZZER, HIGH);  //  sound when ambulance is detected
        } 
        else if (received == 'R') {
            digitalWrite(GREEN_PIN, LOW);
            digitalWrite(RED_PIN, HIGH);
            digitalWrite(BUZZER, LOW);  // Buzzer OFF when no ambulance
            delay(1000);
            digitalWrite(BUZZER, LOW);
        }
    }
}
