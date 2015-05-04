
#include "fdserial.h"
#include "abdrive.h"
#include "simpletools.h"
#include "ping.h"

#include "serialcom.h"
#include "sensor.h"
#include "wander.h"

#define PING_PIN 8
#define LEFT_WHISKER 1
#define RIGHT_WHISKER 0

#define RX_PIN 11//31//11
#define TX_PIN 10//30//10
#define BAUD 9600


int main()
{
  //simpleterm_close(); //close default terminal, I want to use those pins
                      //if the default uart pins are not b nused, this isn't needed
                      
  startComs(RX_PIN, TX_PIN, BAUD, 1000); //this will go to the bluetooth module eventually
  startSensor(PING_PIN, LEFT_WHISKER, RIGHT_WHISKER);
  
  int speed = 20;
  
  int n = 0;
  while(1)                                    
  {
    int command = rxCommand();
    switch(command) //wait for a control byte
    {
      case 'e':
        txInt32(n); //sending incrementing numbers
        n+=10000; 
        break;
      
      case 'b':
        txInt32(rxInt32()*2); //double received number
        break;  
      
      case '?':
        txInt32(42);
        break;
        
      case 'z':
        startWander();
        break;
        
      case 'x':
        stopWander();
        drive_speed(0,0);
        break;
        
      case 'f':
        print("p %d\tpc %d\tpi %d\twl %d\twr %d\ttl %d\ttr %d\n",getPing(), getPingcm(), getPingin(), getWhiskerL(), getWhiskerR(), getTicksL(), getTicksR());
        break;
        
      case 'q':
        drive_speed(0,0);
        break;
        
      case 'w':
        drive_speed(speed,speed);
        break;
      
      case 'a':
        drive_speed(-speed,speed);
        break;
        
      case 's':
        drive_speed(-speed,-speed);
        break;
        
      case 'd':
        drive_speed(speed,-speed);
        break;
        
      case 't':
        if (speed>50) speed =20; else speed =70;
        break;
        
      case -1:    //case when timed out
        txInt32(314);
        break;
        
      default:    //unknown command
        txInt32(2718);
        txInt32(command);
        //print(command);
        print("\n%d\n",command);
    }        
    
    //Note: The computer can sometimes miss bytes 
    //when the bytes are coming really fast 
  }
}
