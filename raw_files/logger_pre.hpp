#pragma once
#ifndef FILENAME_UPPER_REPLACE_H
#define FILENAME_UPPER_REPLACE_H

#include <string>


// X-Macro
#define LOGLVLS \
LOGLVLS_REPLACE

#define LOGLVL(log_level) log_level, 
enum Level {
    LOGLVLS
};
#undef LOGLVL


void Log_Basic(Level level, std::string to_log);
void SetLevel(Level level);
Level GetLevel();


#define LOGLVL(log_level) void\
 Log_##log_level(std::string\
 to_log);
    LOGLVLS
#undef LOGLVL


#endif // FILENAME_UPPER_REPLACE_H