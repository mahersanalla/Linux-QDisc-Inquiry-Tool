#include "QOSInterface/interface.h"
#include <stdio.h>

int main()
{
	setNetDevice("router-server");
	printf ("The size of the queue is: %d\n", printQueueSize());
	return 0;
}
