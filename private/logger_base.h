#pragma once
#ifndef LOGGER_BASE_H
#define LOGGER_BASE_H

#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif




int open_log(const char* filepath, bool overwrite=false);
int write_to_log(const char* log_str, unsigned int len);
int close_log();


#ifdef __cplusplus
}
#endif



#endif // _LOGGER_BASE_H_