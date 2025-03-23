#define BUZZER_PIN 9  // Define the buzzer pin

void setup() {
    pinMode(BUZZER_PIN, OUTPUT);  // Set buzzer pin as output
    digitalWrite(BUZZER_PIN, HIGH); // Turn ON buzzer when power is supplied
}

void loop() {
    // No need to add anything in loop, as the buzzer stays ON
}
