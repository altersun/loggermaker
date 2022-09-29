#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h> 

#include "logger_base.h"

// Set a max log file name size that can be adjusted in Make
#ifndef MAX_LOG_FILE_NAME_LEN
#define MAX_LOG_FILE_NAME_LEN 512
#endif

static char s_log_file_name[MAX_LOG_FILE_NAME_LEN] = {0};
static bool s_log_open = false;


int open_log(const char* filepath, bool overwrite)
{
    int mode = S_IWUSR | S_IWGRP | S_IWOTH;
    int flags = O_WRONLY | O_CREAT;
    if (overwrite) {
        flags |= O_TRUNC;
    } else {
        flags |= O_APPEND;
    }
    
    int fd = open(filepath, flags, mode);
    if (fd < 0) {
        // TODO: Cleaner error reporting
        return fd;
    }


    int ret = lockf(fd, F_TLOCK, 0);
    if (ret != 0) {
        // TODO: Cleaner error reporting
        return ret; // Maybe errno too?
    }
    return 0;
}


int close_log()
{
    close
}


