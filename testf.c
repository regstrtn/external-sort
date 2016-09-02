#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>

int getmachinelist(char *taskfile, char machinenames[][100], int machineinstances[], char tasks[][100], int timereq[], int *numtasks, char semnames[][100]) {
				FILE *fptask = fopen(taskfile, "r");
				fseek(fptask, 0, SEEK_SET);
				char *buffer = NULL;
				size_t bufsize = 0;
				char s[99], m[97], sem[99];
				int bytesread = 0, bytesnow, charsread = 0;
				int machinecount = 0, tasktime=0, totalinstances = 0;
				//struct machinestruct * machinelist = malloc(100*sizeof(machine));
				int i = 0, j = 0, k = 0, r = 0, inst = 0;
				while(getline(&buffer, &bufsize, fptask)>0) {
					sscanf(buffer, "%s %d%n", m, &machinecount, &bytesnow);
					strcpy(machinenames[i], m);
					strcpy(sem, "/"); strcat(sem, m); strcpy(semnames[i], sem); //Semaphore name needs to start with forward slash
					machineinstances[i] = machinecount;
					bytesread = bytesnow;	
					while((charsread = sscanf(buffer+bytesread, "%s %d%n", s, &tasktime, &bytesnow))>0){  
								strcpy(tasks[j], s);
								timereq[j] = tasktime;
								bytesread+=bytesnow;
								j++;
					} i++;
				}
			  *numtasks = j; //Number of task variants
			  for(j=0;j<i;j++) inst+=machineinstances[j]; 
				return inst; //Return total number of instances of all machines put together
}

int main() {
	char machinenames[100][100];
	int nummachines = 0; 
	int machineinstances[100];
	int numinstances = 0;
	int numtasks = 0;
	char semnames[100][100];
	int timereq[1000];
	char tasks[1000][100];
	int jobsdone = 0;
	int jobstoperform = 0;
	int tasksdone[100] = {0};
	char taskfile[100], jobfile[100];
	strcpy(taskfile, "test-2-slave.info");
	getmachinelist(taskfile, machinenames, machineinstances, tasks, timereq, &numtasks,semnames);
}
