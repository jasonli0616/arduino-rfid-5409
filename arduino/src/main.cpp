#include <Arduino.h>
#include <Adafruit_PN532.h>

#define PN532_IRQ 2
#define PN532_RESET 2

Adafruit_PN532 nfc(PN532_IRQ, PN532_RESET);

void setup() {

  Serial.begin(115200);

  // Set up reader
  nfc.begin();
  if (!nfc.getFirmwareVersion()) {
    Serial.println("ERROR: Didn't find PN532 board.");
    while (true) {} // Stop program
  }

  Serial.println("READY");

}

void loop() {

  uint8_t success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };
  uint8_t uidLength;

  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);

  if (success) {

    // Print UID
    Serial.print("SUCCESS: ");
    for (uint8_t i = 0; i < uidLength; i++) {
      Serial.print(uid[i], HEX);
      Serial.print(" ");
    }
    Serial.println();

    // Delay before reading next card
    delay(1000);
  }

}
