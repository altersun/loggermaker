#include <iostream>
#include <vector>


#include "include/FILENAME_REPLACE.hpp"
#include "private/logger_base.h"

namespace {
#define LOGLVL(log_level) #log_level,
    const std::vector<std::string> s_log_levels {
        LOGLVLS
    };
#undef LOGLVL

    SCOPING_NS_REPLACELevel s_current_log_level = INFO;
}

#define LOGLVL(log_level) void\
 OUTER_NAMESPACE_REPLACELog_##log_level(std::string\
 to_log){SCOPING_NS_REPLACELog_Basic(Log::log_level,to_log);}
    LOGLVLS
#undef LOGLVL


void SCOPING_NS_REPLACELog_Basic(SCOPING_NS_REPLACELevel level, std::string to_log)
{
    if (level < s_current_log_level) {
        return;
    }
    
    std::cout << s_log_levels[level] << " " << to_log << std::endl;
}


void SCOPING_NS_REPLACESetLevel(SCOPING_NS_REPLACELevel level)
{
    s_current_log_level = level;
}


SCOPING_NS_REPLACELevel SCOPING_NS_REPLACEGetLevel()
{
    return s_current_log_level;
}