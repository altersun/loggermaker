#include <string>

namespace Spider::Logger {


// X-Macro
#define LOGLVLS \
    LOGLVL(DEBUG) \
    LOGLVL(INFO) \
    LOGLVL(WARNING) \
    LOGLVL(ERROR) \
    LOGLVL(FATAL)

#define LOGLVL(log_level) log_level, 
enum Level {
    LOGLVLS
};
#undef LOGLVL

void Log_Basic(Level level, std::string to_log);
void SetLevel(Level level);


} // end namespace Log


namespace Spider {
    
#define LOGLVL(log_level) void\
 Log_##log_level(std::string\
 to_log);
    LOGLVLS
#undef LOGLVL
}

