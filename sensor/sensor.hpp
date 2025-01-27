/**
   @file sensor.hpp
   @brief Abstracting a temperature sensor
**/
#ifndef TEMPERATURE_H
#define TEMPERATURE_H

//#define TEMPERATURE_REAL // comment to use the "fake" module

void sensor_Init(void);
float temperature_Read(void);
float humidity_Read(void);

#endif
