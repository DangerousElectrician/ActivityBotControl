#include "wander.h"


#define TurnK 35 

static int *cog;

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
      
        int pos = getPingcm(); //update sensor values simultaneously enough.
      
        if (pos > max_distance)            //initial scan
        {
            max_distance= pos;
            index = a;
        }
        pause(25);                        //time to think
      }
  }
   
}

int *startWander()
{
  cog = cog_run(&wander, 100);
  return cog;
}  

void stopWander()
{
  cog_end(cog);
}  