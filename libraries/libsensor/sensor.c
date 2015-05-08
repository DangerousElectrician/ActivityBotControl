
#include "sensor.h"
#include "mstimer.h"

static int *cog=0;

static volatile int ping_Pin, leftWhisker_Pin, rightWhisker_Pin;
static volatile int lTicks, rTicks, pinguS, lWhisker, rWhisker;
static volatile float x,y,th;

int *startSensor(int pingPin, int leftWhiskerPin, int rightWhiskerPin)
{
  if(!cog)
  {
    ping_Pin=pingPin;
    leftWhisker_Pin=leftWhiskerPin;
    rightWhisker_Pin=rightWhiskerPin;
    cog = cog_run( &sensorUpdater,100);
  }
  return cog;
}  

void stopSensor()
{
  cog_end(cog);
  cog = 0;
}  

void sensorUpdater()
{
  int rt=0, lt=0;
  float prt, plt;
  th =0;
  float dth,ds,dx,dy;
  x=0; y=0;
  mstime_start();
  while(1)
  {
    
    pinguS = ping(ping_Pin);
    lWhisker = input(leftWhisker_Pin);
    rWhisker = input(rightWhisker_Pin);
    
    prt = rt;
    plt = lt;
    
    drive_getTicks(&lt, &rt);
    lTicks = lt;
    rTicks = rt;
    
    
    dth = ((rt-prt) -(lt-plt))/33; //32.3077 is the axel length in ticks
    ds  = ((rt-prt) +(lt-plt))/2.0; //distance travelled
    
    dx= ds * cos(th + dth/2.0);
    dy= ds * sin(th + dth/2.0);
    th += dth;
    
    if (th>=2.0*PI) th-=2.0*PI;
    if (th<0) th+=2.0*PI;
    
    x+=dx;
    y+=dy;
    
    while(mstime_get() % 10 != 0);
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

float getXpos()
{
  return x;
}

float getYpos()
{
  return y;
}  

float getThrad()
{
  return th;
}

int getXint()
{
  return (int)x;
}

int getYint()
{
  return (int)y;
}

int getThint()
{
  return (int)th;
}

float getXcm()
{
  return x/3.25;
}

float getYcm()
{
  return y/3.25;
}

float getThdeg()
{
  return (th/(2.0*PI)) * 360.0;
}
  
        