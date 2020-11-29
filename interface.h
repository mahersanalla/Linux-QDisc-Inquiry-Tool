//-- QOS interface between user space and kerenl space.

/**
  * Given a net device name' it sets the net device.
  * Please note that if a faulty net device were given an error will not be detected here
  */
void setNetDevice(char* net_dev_name);

/**
 * Prints the queue size of the previously declared device (by setNetDevice),
 * return value:
 *	-1 - if an error has occured
 * 	 queue_size >= 0 - on success
 * NOTE: Error can occur in the following events - 
 *		1. error triggering on of the module attributes
		2. dev name could not been found
		3. printQueueSize() were called before setNetDevice
 */
int printQueueSize();
