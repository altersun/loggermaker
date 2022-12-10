#! /usr/bin/python3

import argparse
from asyncio.log import logger
import os
import sys
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
    level_list = [f'    LOGLVL({level})' for level in levels]
    return ' \\\n'.join(level_list)


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

    parser = argparse.ArgumentParser(description='Logger settings')
    parser.add_argument('-f', '--config_file', help='Config file which includes settings')
    parser.add_argument('-i', '--inner_namespace', help='Innada;djhad', default='')
    parser.add_argument('-o', '--outer_namespace', default='')
    parser.add_argument('-c', '--clean', default=False, help='Delete generated files')
    # The goal of inner & outer namespaces (IN and ON) is for C++ namespacing
    # It affects the simplified logging functions
    # So if IN has a value and ON does not, all functions will be <IN>::<function>
    # And if ON has a value and ON does not, all functions will be <ON>::<function> EXCEPT Log_<level> which will have no namespace
    # And if ON and IN have value, it will be <IN>::Log_<level> and <ON>::<IN>::<all_other_functions>



    # TODO: These should be arguments or config entries
    filename = 'loggie' 
    levels = ['no_biggie', 'im_worried', 'OH_SNAP']
    logger_options = ['filename', 'linenumber'] # TODO: Support time
    default_level = levels[0]
 
    # Create ouput directory if necessary
    try:
        os.mkdir('./output')
    except FileExistsError:
        pass
    except Exception as e:
        print(f'Cannot create output directory: {e}')
        sys.exit(-1)


    # CPP Header testing
    with open('raw_files/logger_pre.hpp') as cpp_logger_pre:
        cpp_logger_header = cpp_logger_pre.read()

    cpp_logger_header = cpp_logger_header.replace('FILENAME_UPPER_REPLACE', filename.upper())
    cpp_logger_header = cpp_logger_header.replace('LOGLVLS_REPLACE', create_levels(levels))
    
    

    # produce output
    print(f'{cpp_logger_header}\n\n')
    with open(f'./output/{filename}.hpp', 'w') as cpp_logger_header_post:
        cpp_logger_header_post.write(cpp_logger_header)
