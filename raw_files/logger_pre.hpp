#pragma once
#ifndef FILENAME_UPPER_REPLACE_H
#define FILENAME_UPPER_REPLACE_H

#include <string>

NAMESPACE_START_REPLACE

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

NAMESPACE_END_REPLACE

NAMESPACE_OUTER_START_REPLACE

#define LOGLVL(log_level) void\
 Log_##log_level(std::string\
 to_log);
    LOGLVLS
#undef LOGLVL

NAMESPACE_OUTER_END_REPLACE


#endif // FILENAME_UPPER_REPLACE_H