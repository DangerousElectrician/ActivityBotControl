#include "wander.h"

#define TurnK 35 

static int pos;
static int leftEncoder, rightEncoder;

void wander()
{
   int max_distance=0,index=0;
   while(1)
   {
      for(int a=0; a<TurnK; a++)
      {
        drive_speed(15,-15);              // rotate  360 deg
        pause(200);
      
        drive_speed(0,0);                  //stop
        pause(25);
      
        pos = ping(8); //update sensor values simultaneously enough.
        drive_getTicks(&leftEncoder,&rightEncoder);
      
        if (pos > max_distance)            //initial scan
        {
            max_distance= pos;
            index = a;
        }
        pause(25);                        //time to think
      }
  }
   
}

int getPing()
{
  return pos;
}

int getLeftTicks()
{
  return leftEncoder;
}

int getRightTicks()
{
  return rightEncoder;
}    