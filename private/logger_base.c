#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h> 

#include "logger_base.h"

// Set a max log file name size that can be adjusted in Make
#ifndef MAX_LOG_FILE_NAME_LEN
#define MAX_LOG_FILE_NAME_LEN 512
#endif

// Set buffer size and behavior that can be adjusted in Make
#ifndef BUFFER_SIZE
#define BUFFER_SIZE 256
#endif
#ifndef BUFFER_FLUSH_BEHAVIOR
#define BUFFER_FLUSH_BEHAVIOR _IOLBF // Line buffer by default. Choices are Full Buffering (_IOFBF) or No Buffering (_IONBF).
#endif

// Log file pointer
static FILE* s_fp = NULL;

// Buffer for log messages. No need to initialize.
static char s_buffer[BUFFER_SIZE];


bool is_log_open()
{
    return s_fp != NULL;
}


int open_log(const char* filepath, bool overwrite)
{
    // Can't open if we're already open!  
    if (is_log_open()) {
        return -1;
    }

    if (overwrite) {
        s_fp = (filepath, "w");
    } else {
        s_fp = (filepath, "a");
    }
    if (s_fp == NULL) {
        perror("Could not open log file");
        return -1;
    }

    // Try to set buffer size and behavior
    setbuf(s_fp, s_buffer);
    if (0 != setvbuf(s_fp, s_buffer, BUFFER_FLUSH_BEHAVIOR, BUFFER_SIZE)) {
        close_log(s_fp);
        return -1;
    }

    return 0;
}
    

// Made destructor to ensure logs are closed cleanly as possible
int __attribute__((destructor)) close_log()
{
    if (!is_log_open()) {
        return 0;
    }
    
    if (0 != fclose(s_fp)) {
        return -1;
    }
    return 0;
}


int write_to_log(const char* log_str, unsigned int len)
{
    if (!is_log_open()) {
        return -1;
    }
    if (log_str[len] != '\0') {
        // TODO: Remove this debug line
        fputs("OOPS badly terminated string!", s_fp);
        return -1;
    }
    fputs(log_str, s_fp);
    return 0;
}