/**
   @file radio.hpp
   @brief Abstracting the radio modem
**/

#ifndef RADIO_H
#define RADIO_H

bool radio_Init(void);
void radio_Run(void);

void radio_startPayload(uint8_t port);
bool radio_sendPayload(void);

void radio_addUint16_t(uint16_t value);
void radio_addTemperature(float value);
void radio_addCLPPTemperature(uint8_t channel, float value);

void radio_addCLPPHumidity(uint8_t channel, float value);

void radio_addCLPPLedState(uint8_t channel, uint8_t ledState);

int16_t radio_downlinkRead(void);

// provisional
#define OTAA_BAND     (RAK_REGION_EU868)

#endif
