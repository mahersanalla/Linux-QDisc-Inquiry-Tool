#include <stdio.h>
void setNetDevice(char* net_dev_name){
	if(!net_dev_name) return;
	//-- Trigger QOS module <set device> attribute.
	FILE *fpw;
	fpw = fopen("/sys/kernel/QOSInfo/setDevice","w");
	if(fpw == NULL)
	{
		fprintf(stderr, "Error, falied Triggering <set device> attribute\n");
		return;             
	}
	fprintf(fpw,"%s",net_dev_name);
	fclose(fpw);
	return;
}

int printQueueSize(){
	FILE *fp1 = NULL;
	int queue_size = -1;

	//-- Trigger QOS module <get device queue size> attribute.
	fp1= fopen ("/sys/kernel/QOSInfo/getQueueSize", "r");
	if(!fp1)
	{
		fprintf(stderr, "Error, falied Triggering <get queue size> attribute\n");
		return -1;
	}
	while( fscanf(fp1, "%d", &queue_size) == 1 ) { }
	fclose(fp1);
	return queue_size;
}
