#include "pin_define.h"
#include "ruiTop.h"
#include <Arduino.h>
#include "led.hpp"

/*************************************************************************************************/
/**
  * @brief Preparing pin corresponding to LED
  * @return none
  */
void ledInit(void) 
{
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);
}

/*************************************************************************************************/
/**
  * @brief  Turn ON the green LED
  * @return none
  */
void greenLedOn(void)
{
  digitalWrite(GREEN_LED, HIGH);
}


/*************************************************************************************************/
/**
  * @brief  Turn OFF the green LED
  * @return none
  */
void greenLedOff(void) 
{
  digitalWrite(GREEN_LED, LOW);
}


/*************************************************************************************************/
/**
  * @brief  Turn ON the blue LED
  * @return none
  */
void blueLedOn(void) 
{
  digitalWrite(BLUE_LED, HIGH);
}


/*************************************************************************************************/
/**
  * @brief  Turn OFF the blue LED
  * @return none
  */
void blueLedOff(void) 
{
  digitalWrite(BLUE_LED, LOW);
}

/*** End of file *********************************************************************************/
