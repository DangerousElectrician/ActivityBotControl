//AUTONOMOUS ROBOT MAPPING WIRELESS NAVIGATIONATORY ROBOLICIUOS COMPUTATION WONDER-GRAM.
//
#include "wander.h"
#include "serialcom.h"

//Program to control the friken robot to do friken robot stuff. i.e
// wander autonomously and beam data back to the computer when requested.
//need method to communicate with computer
//need method to package sensor data
//need method to wander around
//need override methods for computer.

//pinouts 
/*
  right whisker pin0
  left whisker pin1
  
  ping pin8
  
  bluetooth tx = 10
  bluetooth rx = 11
  
*/

//cores
/*
	one to drive
	one to talk
	one to see
*/

//command set
/*
to be determined
*/

#define RXPIN 11 //11 bulloetoofgh //Rx on bluetooth is Tx from robot
#define TXPIN 10 //10
#define BAUD 9600
#define TOUT 1000
#define true 1 //fuck simple ide

#include "simpletools.h"
#include "abdrive.h"
#include "ping.h"
#include "wander.h"


#include "serialcom.h" //custom library created by Haiming
#include "fdserial.h"

/*void wander() --should just run from main as cog'd
{
      wander();
}
*/

/* --depreceated by wander
void update()
{
  while(true)
  {
    drive_getTicks(&leftTicks, &rightTicks);
    pingMS = ping(8);
    pause(20);
  }  
}
*/


int main()
{
// start movement cog
// cog continously streams data to commuication cog
//communicatoin cog talks to the computer when it needs to
    //simpleterm_close();
    int *cog = cog_run(&wander, 200); //FROM WANDER LIB
    
    
    int command =0;
	  startComs( RXPIN, TXPIN, BAUD, TOUT);
  //simpleterm_open();
  
  
  
	while(true)
	{
		int command = rxCommand();
    
    if (command == 'a')
    {
      txInt32(getLeftTicks()); //FROM WANDER
      txInt32(getRightTicks());
      txInt32(getPing());
      
      txInt32(66); //debug
      
      ////print("idiflis\n");
    }
    else if (command == 'f')
    {
     // something else
      txInt32(71); //debug
      ////print("f reciecved\n");
    }
    else if (command == 'o')
    {
      //something else
      txInt32(80); //debug
      //////print("OOOOHHHHHH RECIEVED!!!\n");
    }
    else if (command ==-1) //you're fucked
    {
      //timeout
      txInt32(64);//debug
      ////////print("loveMEEEEE\\!!!\n");
    }      
	}


}