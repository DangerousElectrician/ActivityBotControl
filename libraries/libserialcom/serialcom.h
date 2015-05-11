
#include "fdserial.h"

/**
 * @brief intializes serial communications.
 * @param rxpin is the pin number to receive on
 * @param txpin is the pin to transmit on
 * @param baudrate is the baud rate
 * @param timeout is how long to wait for a byte to come over the UART in milliseconds
 */
void startComs(int rxpin, int txpin, int baudrate, int timeout);

/**
 *@brief sends a 32 bit signed integer over the UART
 *
 *@param i integer to send
 */
void txInt32(int i);

void txFloat(float f); //send 32-bit float

void txBytes(int n, char *b); //send n bytes

/**
 *@brief receive a byte from the UART. This function is blocking.
 *
 *@returns byte received or -1 if timed out
 */
int rxCommand();

/**
 *@brief receive a 32 bit integer as 4 bytes. Blocking. No error checking. 
 *Make sure sending device will send 4 bytes. Unpredictable on timeout
 *
 *@returns received integer
 */
int rxInt32();

int rxIntn(int n); //receive unsigned int of n bytes

int rxInt8(); //receive signed 8-bit integer