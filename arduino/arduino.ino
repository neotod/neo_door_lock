#include <ArduinoJson.h>

#define LOCK_PIN 4

bool data_ready = false;
String data = "";


void setup() {
    Serial.begin(115200);

    pinMode(LOCK_PIN, OUTPUT);
}

void loop() {
    if (Serial.available()) {
        data = Serial.readString();
        data_ready = true;
    }

    if (data_ready) {
        DynamicJsonDocument doc(512);
        DeserializationError error = deserializeJson(doc, data);

        if (error) {
            data_ready = false;
            return;
        }

        if (doc["type"] == "request") {
            doc["type"] = "response";

            if (doc["data"] == "lock") {
                doc["data"] = "done";
                delay(50);
                serializeJson(doc, Serial);

                digitalWrite(LOCK_PIN, HIGH);
                delay(3000);
                digitalWrite(LOCK_PIN, LOW);
            }

            data_ready = false;
        }

    }
}