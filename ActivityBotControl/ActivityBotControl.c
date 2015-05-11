//libraries
#include "fdserial.h"
#include "abdrive.h"
#include "simpletools.h"
#include "ping.h"
#include "mstimer.h"

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
        
      case '0': //start sensor updater
        startSensor(PING_PIN, LEFT_WHISKER, RIGHT_WHISKER);
        txInt32(42);
        break;
        
      case 128: //stop sensor updater
        stopSensor();
        break;
        
      case 129: //start drive cog
        drive_open();
        txInt32(42);
        break;
        
      case 130:  //stop drive cog
        drive_close();
        break;

      case 'z': //run function "startWander"
        startWander();
        break;
        
      case 'x': //run function "stopWander"
        stopWander();
        drive_speed(0,0);
        break;
        
      case 'f': //send sensor data over usb serial
        print("p %d\tpc %d\tpi %d\twl %d\twr %d\ttl %d\ttr %d\n",getPing(), getPingcm(), getPingin(), getWhiskerL(), getWhiskerR(), getTicksL(), getTicksR());
        break;
     
      case 131: //send sensor data over bluetooth
        {
        txFloat(getXpos());
        txFloat(getYpos());
        txFloat(getThrad());
        txInt32(getTicksL());        
        txInt32(getTicksR());        
        int pung = getPing();
        txBytes(2,&pung);       
        pung =  getWhiskerL()+getWhiskerR()<<2;
        txBytes(1,&pung);
        break;
        }        
      case 132: //recieve drive speed from computer
        drive_speed(rxInt8(),rxInt8());
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
        
      case 'i': // print 
        print("X = %.2f, Y = %.2f, Th = %.1f\n", (double) getXcm(), (double) getYcm(), (double) getThdeg());
        break;
        
      case 'k': //kalibrate
        while(getThdeg()<90)
        {
          drive_speed(-speed,speed);
        }
        drive_speed(0,0);
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
