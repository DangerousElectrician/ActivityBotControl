
#include "serialcom.h"

static fdserial *conn;
static int tout = 1000;

void startComs(int rxpin, int txpin, int baudrate, int timeout)
{
  conn = fdserial_open(rxpin, txpin, 0, baudrate);
  tout = timeout;
}

void txInt32(int i) //sends in little endian
{
  for(int j = 0; j < 4; j++)
  {
    writeChar(conn, (i>>(8*j)) & 0xff);    //& 0xff truncates int from 32 bits to 8 bits
  }                               //bitshifting before truncate gets 4 bytes with the same bits as the int
}

void txFloat(float f)
{
  char *b = &f;
  for(int j = 0; j < 4; j++)
  {
    writeChar(conn, b[j]);
  }
}  

void txBytes(int n, char *b)
{
  for(int j = 0; j < n; j++)
  {
    writeChar(conn, b[j]);
  }
}  

int rxCommand()
{
  return fdserial_rxTime(conn, tout);
}

int rxInt32()
{
  int received = 0;
  for(int j = 0; j < 4; j++)
  {
    received += fdserial_rxTime(conn, tout)<<(8*j);
  }
  return received;
}  