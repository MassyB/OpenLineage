# Copyright 2018-2024 contributors to the OpenLineage project
# SPDX-License-Identifier: Apache-2.0

from typing import Any, Dict, List, Optional


def get_from_nullable_chain(source: Any, chain: List[str]) -> Optional[Any]:
    """
    Get object from nested structure of objects, where it's not guaranteed that
    all keys in the nested structure exist.
    Intended to replace chain of `dict.get()` statements.
    Example usage:
    if not job._properties.get('statistics')\
        or not job._properties.get('statistics').get('query')\
        or not job._properties.get('statistics').get('query')\
            .get('referencedTables'):
        return None
    result = job._properties.get('statistics').get('query')\
            .get('referencedTables')
    becomes:
    result = get_from_nullable_chain(properties, ['statistics', 'query', 'queryPlan'])
    if not result:
        return None
    """
    chain.reverse()
    try:
        while chain:
            next_key = chain.pop()
            if isinstance(source, dict):
                source = source.get(next_key)
            else:
                source = getattr(source, next_key)
        return source
    except AttributeError:
        return None


def get_from_multiple_chains(source: Dict[str, Any], chains: List[List[str]]) -> Optional[Any]:
    for chain in chains:
        result = get_from_nullable_chain(source, chain)
        if result:
            return result
    return None


def parse_single_arg(args, keys: List[str], default=None) -> Optional[str]:
    """
    In provided argument list, find first key that has value and return that value.
    Values can be passed either as one argument {key}={value}, or two: {key} {value}
    """
    for key in keys:
        for i, arg in enumerate(args):
            if arg == key and len(args) > i:
                return args[i + 1]
            if arg.startswith(f"{key}="):
                return arg.split("=", 1)[1]
    return default


def parse_multiple_args(args, keys: List[str], default=None) -> List[str]:
    """
    Given a list of arguments that support syntax such as `--key=value1 value2`
    (like `--model`), return a list of values associated with the given keys.
    """
    parsed_values = []

    for key in keys:
        cur_key = None
        cur_value = None

        for arg in args:
            # `--foo bar baz` case
            if arg == key:
                cur_key = arg
            # `--foo=bar` with single value case
            elif arg.startswith(f"{key}="):
                parsed_values.append(arg.split("=", 1)[1])
            elif cur_key:
                # Done the with current key
                if arg.startswith("-") and cur_key:
                    cur_key = None
                    cur_value = None
                # If we reach here, then arg is the next value for the current key
                else:
                    cur_value = arg

            # Add cur_value only if it's set, if cur_key is set and the argument is
            if cur_key and cur_value:
                parsed_values.append(cur_value)

    return parsed_values or default or []


def add_command_line_arg(command_line: List[str], arg_name: str, arg_value: str):
    command_line = list(command_line)
    arg_name_index = None
    try:
        arg_name_index = command_line.index(arg_name)
    except ValueError:
        # arg_name is not in list
        pass

    if arg_name_index is not None:
        if arg_name_index + 1 >= len(command_line):
            command_line.append(arg_value)
        else:
            command_line[arg_name_index + 1] = arg_value
    else:
        command_line.append(arg_name)
        if arg_value:
            command_line.append(arg_value)

    return command_line


def add_or_replace_command_line_option(
    command_line: List[str], option: str, replace_option: Optional[str] = None
) -> List[str]:
    """
    If replace_option is ignored then the option is simply added
    """
    command_line = list(command_line)
    if replace_option:
        try:
            replace_option_index = command_line.index(replace_option)
            command_line[replace_option_index] = option
        except ValueError:
            command_line.append(option)
    else:
        command_line.append(option)

    return command_line


def stream_has_lines(stream):
    """
    Checks if the given stream has lines or not
    """
    current_position = stream.tell()
    has_lines = len(stream.readlines()) > 0
    stream.seek(current_position)
    return has_lines
