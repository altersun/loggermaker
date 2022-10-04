#! /usr/bin/python3

from typing import List


StrList = List[str]


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
        '#include <iostream>',
        '#include <vector>',
        f'#include "{filename}.hpp"',
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


if __name__ == '__main__':

    # TODO: These should be arguments
    filename = 'loggie'
    levels = ['no_biggie', 'im_worried', 'OH_SNAP']
    default_level = levels[0]

    # CPP version for testing
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

    # CPP Version for testing
    cpp_source_output_list = [
        create_includes_cpp(filename),
        create_levels_container_cpp(default_level),
    ]
    cpp_source_output = '\n\n'.join(cpp_source_output_list)


    # produce output
    print(f'{cpp_header_output}\n\n')
    print(f'{cpp_source_output}\n\n')