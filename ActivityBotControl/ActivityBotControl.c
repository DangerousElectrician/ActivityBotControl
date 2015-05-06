//libraries
#include "fdserial.h"
#include "abdrive.h"
#include "simpletools.h"
#include "ping.h"

#include "serialcom.h"
#include "sensor.h"
#include "wander.h"
//define pins of sensors
#define PING_PIN 8
#define LEFT_WHISKER 0
#define RIGHT_WHISKER 1

#define RX_PIN 11   //31 serial //11 bluetooth
#define TX_PIN 10   //30 serial //10 bluetooth
#define BAUD 9600


int main()
{
  //simpleterm_close(); //close default terminal, I want to use those pins
                      //if the default uart (Universal Asynchronous Recieve and Transmitting
                      // pins are not being used, this isn't needed
                      
  startComs(RX_PIN, TX_PIN, BAUD, 1000); //this will go to the bluetooth module eventually
//  startSensor(PING_PIN, LEFT_WHISKER, RIGHT_WHISKER);
  
  int speed = 20; //intial speed 20 ticks/s
  
  int n = 0;
  while(1)       //repeat until power loss                             
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
      
      case '?': //send 42
        txInt32(42);
        break;
        
      case '0':
        startSensor(PING_PIN, LEFT_WHISKER, RIGHT_WHISKER);
        break;

      case 'z': //run function "startWander"
        startWander();
        break;
        
      case 'x': //run function "stopWander"
        stopWander();
        drive_speed(0,0);
        break;
        
      case 'f': //send sensor data
        print("p %d\tpc %d\tpi %d\twl %d\twr %d\ttl %d\ttr %d\n",getPing(), getPingcm(), getPingin(), getWhiskerL(), getWhiskerR(), getTicksL(), getTicksR());
        break;
     
      case 'v':
        txInt32(getTicksL());        
        txInt32(getTicksR());        
        txInt32(getPing());        
        txInt32(getWhiskerL());        
        txInt32(getWhiskerR());
        break;
        
      case 'h': //recieve drive speed from computer
        drive_speed(rxInt32(),rxInt32());
        break;
     
      case 'p':
        __builtin_propeller_clkset(0x80); //reboot
        break;

      case 'q': //stop movement
        drive_speed(0,0);
        break;
        
      case 'w': //move forward
        drive_speed(speed,speed);
        break;
      
      case 'a': //pivot left
        drive_speed(-speed,speed);
        break;
        
      case 's': //move backward
        drive_speed(-speed,-speed);
        break;
        
      case 'd': //pivot right
        drive_speed(speed,-speed);
        break;
      
      case 't': //toggle turbo mode up to 70 ticks/s
        if (speed>50) speed = 20; else speed =70;
        break;
        
      case 'j': //computer input for rotation
        drive_goto(rxInt32(),rxInt32());
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
