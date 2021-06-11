#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>


#define WEBSERVER_PORT 80
#define GPIO2 2
#define MAX_WAIT_COUNTER 20

#define HTTP_INTERNAL_SERVER_ERROR 500
#define HTTP_BAD_REQUEST 401


void index_handle();
void lock_handle();


ESP8266WebServer server(WEBSERVER_PORT);

const char* AP_SSID = "ESP";
const char* AP_PASS = "ThisIsESP8266";


void setup()
{
    Serial.begin(115200);

    pinMode(GPIO2, OUTPUT);
    WiFi.mode(WIFI_AP);
    WiFi.softAP(AP_SSID, AP_PASS);

    server.on("/", HTTP_GET, index_handle);
    server.on("/index", HTTP_GET, index_handle);
    server.on("/lock", HTTP_POST, lock_handle);

    server.begin();
}

void loop()
{
    server.handleClient();
}

void index_handle() {
    digitalWrite(GPIO2, HIGH);
    delay(300);
    digitalWrite(GPIO2, LOW);
    
    String html = "<span>Hi from earth!</span>";
    server.send(200, "text/html", html);
}

void lock_handle() {
    if (!server.hasArg("value")) {
        server.send(HTTP_BAD_REQUEST);
        return;
    }

    String value = server.arg("value");

    StaticJsonDocument<256> doc;
    doc["type"] = "request";
    doc["data"] = value;
    serializeJson(doc, Serial);

    bool result = confirmation_wait();

    if (result)
        server.send(200);
    else
        server.send(HTTP_INTERNAL_SERVER_ERROR);
}

bool confirmation_wait() {
    String data ="";
    bool data_ready = false;
    bool success = true;
    int wait_counter = MAX_WAIT_COUNTER;

    delay(200);

    while(1) { // waiting for confirmation
        if (Serial.available()) {
            data = Serial.readString();
            data_ready = true;

            digitalWrite(GPIO2, HIGH); // a signal
            delay(300);
            digitalWrite(GPIO2, LOW);
        }

        if (data_ready) {
            StaticJsonDocument<256> doc;
            DeserializationError error = deserializeJson(doc, data); // error-prone: maybe it's better to make a new doc or empty prev doc
            if (error) {
                success = false; // internal server error
            }
            else {
                if (doc["type"] == "response") {
                    if (doc["data"] == "done") {
                        success = true; // success, redirect to home
                        break;
                    }
                }
            }
            data_ready = false; // because data can be gibberish
        }
        else {
            wait_counter--;

            if (wait_counter == 0) {
                success = false; // internal server error
                break;
            }
            delay(200);
        }
    }

    return success;
}
