#include "sensor.h"

#define PING_PIN 8
#define LEFT_WHISKER 1
#define RIGHT_WHISKER 0

int main(void)
{
  startSensor(PING_PIN, LEFT_WHISKER, RIGHT_WHISKER);
  drive_speed(15,-15);
  while(1)
  {
    print("p %d\tpc %d\tpi %d\twl %d\twr %d\ttl %d\ttr %d\n",getPing(), getPingcm(), getPingin(), getWhiskerL(), getWhiskerR(), getTicksL(), getTicksR());
    pause(50);
  }    
}

