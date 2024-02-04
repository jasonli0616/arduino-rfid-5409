#include <Arduino.h>
#include <Adafruit_PN532.h>

#define PN532_IRQ 2
#define PN532_RESET 2

Adafruit_PN532 nfc(PN532_IRQ, PN532_RESET);

void setup() {

  Serial.begin(9600);

  while (true) {

    // Set up reader
    nfc.begin();
    if (nfc.getFirmwareVersion()) {
      // Success
      break;
    }

    Serial.println("ERROR: Didn't find PN532 board.");

  }

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

}

void loop() {
  Serial.println("READY");

  uint8_t success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };
  uint8_t uidLength;

  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength, 500);

  if (success) {

    // Print UID
    Serial.print("SCAN: ");
    for (uint8_t i = 0; i < uidLength; i++) {
      Serial.print(uid[i], HEX);
      Serial.print(" ");
    }
    Serial.println();

    // Delay before reading next card
    delay(1000);
  }

}
