/**
 * @file sensor.cpp
 * 
 */

#include <stdint.h>
#include "sensor.hpp"
#include "rak1901.h"

rak1901 rak1901;

void sensor_Init(void)
{
    // begin for I2C
    Wire.begin();

    // check if snesor Rak1901 is work
    rak1901.init();
}

float temperature_Read(void) 
{
    float temp = NULL;

    if (rak1901.update()) 
    {
        temp = rak1901.temperature();
    } else 
    {
        temp = NULL;
    }
    
    return temp;
}

float humidity_Read(void) 
{
    float hum = NULL;

    if (rak1901.update()) 
    {
        hum = rak1901.humidity();
    } else 
    {
        hum = NULL;
    }
    
    return hum;
}