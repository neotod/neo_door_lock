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
void gsm_handle();
void wifi_handle();


ESP8266WebServer server(WEBSERVER_PORT);

const char* AP_SSID = "ESP";
const char* AP_PASS = "ThisIsESP8266";

int WIFI_IP[4] = {192, 168, 1, 20};
int WIFI_GATE[4] = {192, 168, 1, 9};
int WIFI_SUB[4] = {255, 255, 255, 0};


void setup()
{
    Serial.begin(115200);

    pinMode(GPIO2, OUTPUT);
    WiFi.mode(WIFI_AP);
    WiFi.softAP(AP_SSID, AP_PASS);

    server.on("/", HTTP_GET, index_handle);
    server.on("/index", HTTP_GET, index_handle);
    server.on("/lock", HTTP_GET, lock_handle);
    server.on("/gsm", HTTP_POST, gsm_handle);
    server.on("/wifi", HTTP_POST, wifi_handle);

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
    digitalWrite(GPIO2, HIGH);
    delay(300);
    digitalWrite(GPIO2, LOW);

    StaticJsonDocument<256> doc;
    doc["type"] = "request";
    doc["module"] = "lock";
    doc["result"] = "";
    serializeJson(doc, Serial);

    delay(1000);
    bool result = confirmation_wait();

    if (result)
        server.send(200);
    else
        server.send(HTTP_INTERNAL_SERVER_ERROR);
}

void gsm_handle() {
    if (!server.hasArg("text")) {
        server.send(HTTP_BAD_REQUEST, "text/html", "please provide text");
        return;
    }
    else if (!server.hasArg("number")) {
        server.send(HTTP_BAD_REQUEST, "text/html", "please provide number => ex: 9035315000");
        return;
    }

    String text = server.arg("text");
    String number = server.arg("number");

    if (number.length() != 10) {
        server.send(HTTP_BAD_REQUEST, "text/html", "please provide a valid number => ex: 9035315000");
        return;
    }

    StaticJsonDocument<512> doc;
    doc["type"] = "request";
    doc["module"] = "gsm";
    doc["text"] = text;
    doc["number"] = number;
    doc["result"] = "";
    serializeJson(doc, Serial);

    bool result = confirmation_wait();

    if (result)
        server.send(200);
    else
        server.send(HTTP_INTERNAL_SERVER_ERROR);
}

void wifi_handle() {
    if (!server.hasArg("ssid")) {
        server.send(HTTP_BAD_REQUEST, "text/html", "please provide the ssid");
        return;
    }
    else if (!server.hasArg("password")) {
        server.send(HTTP_BAD_REQUEST, "text/html", "please provide the password");
        return;
    }
  
    const char* wifi_ssid = server.arg("ssid").c_str();
    const char* wifi_pass = server.arg("password").c_str();
    
    server.send(200, "text/html", "Please wait until ESP changes its mode to Station mode.");

    if (WiFi.getMode() != WIFI_STA)
        WiFi.mode(WIFI_STA);

    IPAddress staticIP(WIFI_IP[0], WIFI_IP[1], WIFI_IP[2], WIFI_IP[3]);
    IPAddress gateway(WIFI_GATE[0], WIFI_GATE[1], WIFI_GATE[2], WIFI_GATE[3]);
    IPAddress subnet(WIFI_SUB[0], WIFI_SUB[1], WIFI_SUB[2], WIFI_SUB[3]);

    WiFi.config(staticIP, gateway, subnet);
    WiFi.begin(wifi_ssid, wifi_pass);
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
                    if (doc["result"] == "done") {
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
