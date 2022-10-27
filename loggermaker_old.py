#! /usr/bin/python3

import argparse
from typing import List


StrList = List[str]

# TODO: Make a generic one then a C one
LOG_OPTIONS_LOOKUP_CPP = {
    'filename' : '__FILE__',
    'linenumber' : '__LINE__',
}


RESTRICTED_STRINGS = [
    'FILENAME_UPPER_REPLACE',
    'FILENAME_UPPER_REPLACE_H'
]


def start_header_guard(filename: str) -> str:
    header_guard_list = [
        '#pragma once',
        f'#ifndef {filename.upper()}_H',
        f'#define {filename.upper()}_H',
    ]
    return '\n'.join(header_guard_list)






def create_levels(levels: StrList) -> str:
    # The trailing spaces are important
    level_list = [f'\ \n  LOGLVL({level}) ' for level in levels]
    level_list.insert(0, '#define LOGLVLS ') 
    return ''.join(level_list)


def create_enum() -> str:
    level_enum_list = [
        '#define LOGLVL(log_level) log_level,',
        'enum LogLevel {',
        '    LOGLVLS',
        '};',
        '#undef LOGLVL'
    ]
    return '\n'.join(level_enum_list)


def end_header_guard(filename: str) -> str:
    return f'#endif // {filename.upper()}_H'


def create_header_includes_cpp() -> str:
    return '#include <string>'


def create_base_functions_cpp() -> str:
    basic_functions_list = [
        'void Log_Basic(Level level, std::string to_log);',
        'void SetLevel(Level level);',
        'Level GetLevel();',
    ]
    return '\n'.join(basic_functions_list)


def create_specific_functions_cpp() -> str:
    basic_functions_list = [
        '#define LOGLVL(log_level) void\\',
        ' Log_##log_level(std::string\\',
        ' to_log);',
        '    LOGLVLS',
        '#undef LOGLVL',
    ]
    return '\n'.join(basic_functions_list)


def create_includes_cpp(filename: str) -> str:
    includes_list = [
        '#include <sstream>',
        '#include <vector>',
        f'#include "{filename}.hpp"',
        '#include "logger_base.h"',
    ]
    return '\n'.join(includes_list)


def create_levels_container_cpp(default_level: str) -> str:
    levels_container_list = [
        'namespace {',
        '#define LOGLVL(log_level) #log_level,',
        '    const std::vector<std::string> s_log_levels {',
        '        LOGLVLS',
        '    };',
        '#undef LOGLVL',
        f'    LogLevel s_current_log_level = {default_level};',
        '}',
    ]
    return '\n'.join(levels_container_list)


def define_base_log_function_cpp(log_options: StrList, throw_on_error: bool = True) -> str:
    log_option_list = [LOG_OPTIONS_LOOKUP_CPP[option] for option in log_options]
    log_option_str = ' << '.join(log_option_list)
    log_function_list = [
        'void Log_Basic(Level level, std::string to_log)',
        '{',
        '    if (level < s_current_log_level) {',
        '        return;',
        '    }',
        '    std::stringstream log_stream;',
        f'    log_stream << {log_option_str} << s_log_levels[level] << " " << to_log << std::endl;',
    ]
    if throw_on_error: 
        log_function_list += [
            '    if (write_to_log(log_stream.str().data(), log_stream.str().length()) != 0)',
            '        throw std::runtime_error("Failed to log string"+log_stream.str().data()""with err code"+',
        ]
    else:
        pass
        
        
    log_function_list.append('}') 
    
    return '\n'.join(log_function_list)


def define_specific_functions_cpp() -> str:
    log_functions_list = [
        '#define LOGLVL(log_level) void\\',
        ' Log_##log_level(std::string\\',
        ' to_log){Log_Basic(log_level,to_log);}',
        '   LOGLVLS',
        '#undef LOGLVL',
    ]
    return '\n'.join(log_functions_list)


def define_level_set_n_get() -> str:
    level_setget_list = [
        'void SetLevel(Level level)',
        '{',     
        '    s_current_log_level = level;',
        '}',
        '',
        'Level GetLevel()',
        '{',
        '    return s_current_log_level;',
        '}',
    ]
    return '\n'.join(level_setget_list)


if __name__ == '__main__':

    #parser = argparse.ArgumentParser(description='Logger settings')
    #parser.add_argument()

    # TODO: These should be arguments
    filename = 'loggie' 
    levels = ['no_biggie', 'im_worried', 'OH_SNAP']
    logger_options = ['filename', 'linenumber'] # TODO: Support time
    default_level = levels[0]

    # CPP header for testing
    cpp_header_output_list = [
        start_header_guard(filename),
        create_header_includes_cpp(),
        create_levels(levels),
        create_enum(),
        create_base_functions_cpp(),
        create_specific_functions_cpp(),
        end_header_guard(filename),
    ]
    cpp_header_output = '\n\n'.join(cpp_header_output_list)

    # CPP source for testing
    cpp_source_output_list = [
        create_includes_cpp(filename),
        create_levels_container_cpp(default_level),
        define_base_log_function_cpp(logger_options),
        define_specific_functions_cpp(),
        define_level_set_n_get(),
    ]
    cpp_source_output = '\n\n'.join(cpp_source_output_list)

    # produce output
    print(f'{cpp_header_output}\n\n')
    print(f'{cpp_source_output}\n\n')
