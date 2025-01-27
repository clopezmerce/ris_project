/***
 *  This example shows LoRaWan protocol joining the network in OTAA mode, class A, region EU868.
 *  Device will send uplink every 20 seconds.
***/

#include "led.hpp"
#include "sensor.hpp"
#include "credentials.h"
#include "radio.hpp"

#define MEASUREMENT_PERIOD   (120000)
#define LENGTH 5 
#define MAX_TEMP 25
#define MIN_TEMP -10.0
#define MAX_HUM 80
#define MIN_HUM 20

// Global variables
float lastTemperature[LENGTH];
float lastHumidity[LENGTH];
uint8_t cont = 0;

void setup()
{
  // Initializing the RAK node
  Serial.begin(115200, RAK_AT_MODE);
  delay(5000);

  Serial.println("RAKwireless LoRaWan OTAA Example");
  Serial.println("------------------------------------------------------");

  // Initializing other things
  ledInit();
  radio_Init();
  sensor_Init();
}

void loop()
{
  static uint64_t last = 0;
  static uint64_t elapsed;
  float temperature, humidity;
  uint8_t ledState;

  if ((elapsed = millis() - last) > MEASUREMENT_PERIOD) 
  {
    // Reading the temperature and the humidity values from the sensor
    temperature = temperature_Read();
    humidity = humidity_Read();

    // Storaging those values in a LENGTH-size circular buffer
    lastTemperature[cont] = temperature;
    lastHumidity[cont] = humidity;

    // Printing the arrays
    Serial.println("cont = " + String(cont));
    listArray(lastTemperature);
    listArray(lastHumidity);

    // Updating the counter
    cont++;
    cont = cont % LENGTH;

    // If half of the temperature or the humidity values stored 
    // exceed the maximun level or stay below the minimum it is 
    // turned on the green led
    uint8_t contTempMax = 0;
    uint8_t contTempMin = 0;
    uint8_t contHumMax = 0; 
    uint8_t contHumMin = 0; 

    for (uint8_t i = 0; i < LENGTH; i++)
    {
      if (lastTemperature[i] >= MAX_TEMP) 
      {
        contTempMax++;
      } else if (lastTemperature[i] <= MIN_TEMP) 
      {
        contTempMin++;
      }

      if (lastHumidity[i] >= MAX_HUM) 
      {
        contHumMax++;
      } else if (lastHumidity[i] <= MIN_HUM && lastHumidity[i] > 0)
      {
        contHumMin++;
      }
    }

    uint8_t half = LENGTH / 2;
    if (contTempMax > half || contTempMin > half || contHumMax > half || contHumMin > half) 
    {
      greenLedOn();
      ledState = 1;
    } else 
    {
      greenLedOff();
      ledState = 0;
    }

    //Sending the payload
    radio_startPayload(66);
    radio_addCLPPTemperature(1, temperature);  // CHannel 1: Temperature
    radio_addCLPPHumidity(2, humidity);        // Channel 2: Humidity
    radio_addCLPPLedState(3, ledState);        // Channel 3: Led state
    radio_sendPayload();   /*** falta probar lo de que la conexion sea asincrona */

    //Updating the timer
    last = millis();
  }

  // Reading posible downlinks from the dashboard
  int16_t downlinkData = radio_downlinkRead();

  // If it is received a 01 payload from the dowlink, we must 
  // turn on the control light (blue led)
  // 00 to turn off
  if (downlinkData != -1) 
  {
    Serial.print("Downlink recibido: ");
    Serial.println(downlinkData);
    if (downlinkData == 0) 
    {
      blueLedOff();
      ledState = 0;
    } else if (downlinkData == 1) 
    {
      blueLedOn();
      ledState = 1;
    }
  }

  //Serial.printf("Try sleep %ums..", MEASUREMENT_PERIOD);
  api.system.sleep.all(MEASUREMENT_PERIOD); /* esto creo que esta mal energeticamente, creo que se despierta la cpu cuando sale el paquyete */
  //api.system.sleepFor(MEASUREMENT_PERIOD - (millis() - last))
  //Serial.println("Wakeup..");
}

// Listing the elements of the array on the Serial Monitor
void listArray(float* array) 
{
  for (uint8_t i = 0; i < LENGTH; i++) 
  {
    Serial.print(String(*(array + i)) + " ");
  }
  Serial.println("");
}
