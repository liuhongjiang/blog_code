#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

int getlock(int fd){
    static struct flock lock;
  
    lock.l_type = F_WRLCK;
    lock.l_start = 0;
    lock.l_whence = SEEK_SET;
    lock.l_len = 0;
    lock.l_pid = getpid();
  
    int ret = fcntl(fd, F_GETLK, &lock);
    printf("Return value of fcntl:%d\n",ret);
    if (lock.l_type == F_UNLCK){
        printf("file is not locked\n");
    }
    else {
        printf("file is locked\n");
    }
}
  
int main(int argc, char **argv) {
  if (argc > 1) {
    int fd = open(argv[1], O_WRONLY);
    if(fd == -1) {
      printf("Unable to open the file\n");
      exit(1);
    }
    getlock(fd);
    close(fd);
   
    fd = open("abcd", O_WRONLY | O_CREAT, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP);
    if(fd == -1) {
      printf("Unable to open the file\n");
      exit(1);
    }
    close(fd);
    remove(argv[1]);
    rename("abcd", argv[1]);
    printf("the file is removed and a new file is create\n");
    
    fd = open(argv[1], O_WRONLY);
    if(fd == -1) {
      printf("Unable to open the file\n");
      exit(1);
    }
    getlock(fd);

    // lock it
    fd = open(argv[1], O_WRONLY);
    if(fd == -1) {
      printf("unable to open the file\n");
      exit(1);
    }
    static struct flock lock;
  
    lock.l_type = F_WRLCK;
    lock.l_start = 0;
    lock.l_whence = SEEK_SET;
    lock.l_len = 0;
    lock.l_pid = getpid();
  
    int ret = fcntl(fd, F_SETLKW, &lock);
    printf("Return value of fcntl:%d\n",ret);
    if(ret==0) {
      while (1) {
          sleep(5);
      }
    }
    close(fd);
  }
}
