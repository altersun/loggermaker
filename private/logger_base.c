#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h> 

#include "logger_base.h"

// Set a max log file name size that can be adjusted in Make
#ifndef MAX_LOG_FILE_NAME_LEN
#define MAX_LOG_FILE_NAME_LEN 512
#endif

#define LOG_FD_CLOSED -100

static char s_log_file_name[MAX_LOG_FILE_NAME_LEN] = {0};
static bool s_log_open = false;
static int s_fd = 0;


int open_log(const char* filepath, bool overwrite)
{
    if (s_log_open) {
        // Don't reopen, just skip
        return 0;
    }
    
    // Common permissions, write only, and create if not there
    int mode = S_IWUSR | S_IWGRP | S_IWOTH;
    int flags = O_WRONLY | O_CREAT;
    if (overwrite) {
        flags |= O_TRUNC; // Truncate; overwrite existing contents
    } else {
        flags |= O_APPEND; // Append to existing contents
    }
    
    int open_ret = open(filepath, flags, mode);
    if (open_ret < 0) {
        // TODO: Cleaner error reporting
        return open_ret;
    }
    s_fd = open_ret;

    int lock_ret = lockf(s_fd, F_TLOCK, 0);
    if (lock_ret != 0) {
        // TODO: Cleaner error reporting
        return lock_ret; // Maybe errno too?
    }
    s_log_open = true;
    return 0;
}


int close_log()
{
    if (!s_log_open) {
        return 0;
    }
    int ret = close(s_fd);
    if (ret != 0) {
        return ret;
    }
    s_log_open = false;
    return 0;
}


int write_to_log(const char* log_str, unsigned int len)
{
    // TODO: Finish this
    return 0;
}