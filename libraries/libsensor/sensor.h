//sensor.h
#include "simpletools.h"
#include "abdrive.h"
#include "ping.h"

int getPing();

int getPingcm();

int getPingin();

int getTicksL();

int getTicksR();

int getWhiskerL();

int getWhiskerR();

void startSensor(int pingPin, int leftWhiskerPin, int rightWhiskerPin);

void sensorUpdater();