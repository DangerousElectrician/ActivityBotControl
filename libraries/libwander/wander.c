#include "wander.h"
#include "mstimer.h"


#define TurnK 35 

static int *cog =0;

int spin2find() //spins to find furthest distance
{
      high(26);
      int max_distance =0;
      int index =0;
  
      for(int a=0; a<TurnK; a++)
      {
        drive_speed(15,-15);              // rotate  like 10 deg
        pause(200);
      
        drive_speed(0,0);                  //stop
        pause(25);
      
        int pos = getPingcm();
      
        if (pos > max_distance)            //initial scan
        {
            max_distance= pos;
            index = a;
        }
        pause(25);                        //time to think
      }
      low(26);
      return index;
}

void go2index(int index)
{
      high(27);
        for(int a=0; a<=index; a++)
      {
        drive_speed(15,-15);              // rotate  like 10 deg
        pause(200);
      
        drive_speed(0,0);                  //stop
        pause(50);
      }
      low(27);
} 

void charge2stop()
{
  high(26);
  high(27);
  drive_speed(20,20);
  while (1)
  {
    if (getWhiskerL() ==0 || getWhiskerR() ==0)
    {
      drive_speed(-10,-10);
      pause(1000);
      low(26);
      low(27);
      return;
    } 
    
    if (getPingcm() <= 5)
    {
      drive_speed(-10,-10);
      pause(1000);
      low(26);
      low(27);
      return;
    }    
  }
}  

void wander()
{
  while(1)
  {
    go2index(spin2find());
    charge2stop();
  }               
}

int *startWander()
{
  if (cog ==0) cog = cog_run(&wander, 100); //make sure multiple instances of wander don't run
  return cog;
}  

void stopWander()
{
  cog_end(cog);
  cog =0;
}  