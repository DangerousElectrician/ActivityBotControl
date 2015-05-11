//Localization and Mapping with Wireless Control
//sensor.h
#include "simpletools.h"
#include "abdrive.h"
#include "ping.h"


int getPing(); //get ping sensor data in microseconds

int getPingcm(); //get ping sensor data in centimeters

int getPingin(); //get ping sensor data in inches

int getTicksL(); //get ticks of left wheel

int getTicksR(); //get ticks of right wheel

int getWhiskerL(); //get left whisker state

int getWhiskerR(); //get right whisker state

int *startSensor(int pingPin, int leftWhiskerPin, int rightWhiskerPin); //start sensor updater

void stopSensor(); //stop sensor updater

void sensorUpdater();  //sensor updater function, runs in own cog


float getXpos(); //get x position in ticks

float getYpos(); //get y position in ticks

float getTh();  //get theta of robot in radians


int getXint(); //get x position in integer ticks

int getYint(); //get x position in integer ticks

int getThint();   //get integer theta of robot


float getXcm(); //get x position in centimeters 

float getYcm();  //get y position in centimeters

float getThdeg();  //get theta of robot in degrees