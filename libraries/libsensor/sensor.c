
#include "sensor.h"

static int *cog=0;

static volatile int ping_Pin, leftWhisker_Pin, rightWhisker_Pin;
static volatile int lTicks, rTicks, pinguS, lWhisker, rWhisker;

int *startSensor(int pingPin, int leftWhiskerPin, int rightWhiskerPin)
{
  if(!cog)
  {
  ping_Pin=pingPin;
  leftWhisker_Pin=leftWhiskerPin;
  rightWhisker_Pin=rightWhiskerPin;
  cog = cog_run( &sensorUpdater,100);
  }
}  

void stopSensor()
{
  cog_end(cog);
  cog = 0;
}  

void sensorUpdater()
{
  while(1)
  {
    pinguS = ping(ping_Pin);
    lWhisker = input(leftWhisker_Pin);
    rWhisker = input(rightWhisker_Pin);
    
    int rt, lt;
    drive_getTicks(&lt, &rt);
    lTicks = lt;
    rTicks = rt;
    
    pause(10);
  }    
}  

int getPing()
{
  return pinguS;
}

int getPingcm()
{
  return pinguS/58;
}

int getPingin()
{
  return pinguS/148;
}

int getTicksL()
{
  return lTicks;
}


int getTicksR()
{
  return rTicks;
}


int getWhiskerL()
{
  return lWhisker;
}


int getWhiskerR()
{
  return rWhisker;
}
