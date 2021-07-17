#include <ArduinoJson.h>
#include <SoftwareSerial.h>

#define GSM_RX 2
#define GSM_TX 3

#define LOCK_PIN 7

bool data_ready = false;
String data = "";

SoftwareSerial gsm_serial(GSM_RX, GSM_TX);

void setup() {
    Serial.begin(115200);
    gsm_serial.begin(9600);

    pinMode(LOCK_PIN, OUTPUT);
}

void loop() {
    if (Serial.available()) {
        digitalWrite(LOCK_PIN, HIGH);
        delay(100);
        digitalWrite(LOCK_PIN, LOW);
        
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

            if (doc["module"] == "lock") {
                doc["result"] = "done";
                delay(50);
                serializeJson(doc, Serial);

                digitalWrite(LOCK_PIN, HIGH);
                delay(3000);
                digitalWrite(LOCK_PIN, LOW);
            }
            else if (doc["module"] == "gsm") {
                doc["result"] = "done";
                delay(50);
                serializeJson(doc, Serial);
                delay(500);

                String number = doc["number"];
                String send_inst = "AT+CMGS=\"" + number + "\"";
                String text = doc["text"];
                
                gsm_serial.println("AT");
                delay(100);
              
                gsm_serial.println("AT+CMGF=1");
                delay(100);
                gsm_serial.println(send_inst);
                delay(100);
                gsm_serial.print(text);
                delay(100);
                gsm_serial.write(26);
                
                delay(500);
            }

            data_ready = false;
        }

    }
}
