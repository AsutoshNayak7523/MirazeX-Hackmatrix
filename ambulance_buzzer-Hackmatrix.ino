const int led1 = 9;
const int led2 = 10;
const int led3 = 11;

void setup() {
    Serial.begin(9600);
    pinMode(led1, OUTPUT);
    pinMode(led2, OUTPUT);
    pinMode(led3, OUTPUT);
}

void loop() {
    if (Serial.available() > 0) {
        int soundClass = Serial.parseInt();
        Serial.print("Received: ");
        Serial.println(soundClass);

        // Turn OFF all LEDs first
        digitalWrite(led1, LOW);
        digitalWrite(led2, LOW);
        digitalWrite(led3, LOW);

        // Turn ON LEDs based on classification
        if (soundClass == 1) {
            digitalWrite(led1, HIGH);
        } else if (soundClass == 2) {
            digitalWrite(led1, HIGH);
            digitalWrite(led2, HIGH);
        } else if (soundClass == 3) {
            digitalWrite(led1, HIGH);
            digitalWrite(led2, HIGH);
            digitalWrite(led3, HIGH);
        }
    }
}
