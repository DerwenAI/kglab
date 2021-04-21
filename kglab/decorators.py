#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
## Decorator to handle multiple paths

from copy import deepcopy
#from functools import reduce
from functools import wraps
from glob import glob
import inspect
import pathlib
import typing
import urlpath  # type: ignore


def _test_path (
    path: typing.Union[ pathlib.Path, urlpath.URL ]
    ) -> bool:
    """
Semi-private function to test whether the given path parameter is an
instance of `pathlib.Path`, `urlpath.URL`, or a related class.

    path:
parameter to be tested

    returns:
test condition
    """
    return isinstance(path, (pathlib.Path, urlpath.URL))


def multifile (
    param_name: str = "path",
    ) -> typing.Any:
    """
Creates a wrapper around a read function to read multiple files, given
a glob pattern with at least one wildcard in the path.

    param_name:
parameter to be overloaded

    returns:
constructed decorator
    """

    def decorator (
        f: typing.Any,
        ) -> typing.Any:
        sig = inspect.signature(f)

        if param_name not in sig.parameters:
            raise ValueError(
                f"Reader function {f.__name__} has no parameter '{param_name}'"
            )

        @wraps(f)
        def wrapper (  # pylint: disable=R1710
            *args: typing.Any,
             **kwargs: typing.Any,
             ) -> typing.Any:
            bound_arguments = sig.bind(*args, **kwargs)
            bound_arguments.apply_defaults()

            path = bound_arguments.arguments[param_name]
            path_list: typing.List = []

            # if `*` is not in the path then simply let the default
            # function handle it
            if isinstance(path, str):
                if "*" not in path:
                    return f(*args, **kwargs)

                # initialize the path list with a parsed glob
                path_list = glob(path)

            # also handle single Path objects by the default function
            elif _test_path(path):
                return f(*args, **kwargs)

            # no files were found in the given pattern so raise error
            if len(path_list) == 0:
                raise ValueError(f"No files found in given path list: {path}")

            # handle a list of Path objects
            if isinstance(path, (list)):
                for p in path:
                    if _test_path(path):
                        path_list.append(p)
                    else:
                        raise ValueError(f"Invalid path: {p}")
            else:
                raise ValueError(
                    f"{path} is not a valid string, Path, or list of Paths"
                )

            # store the parsed clumpers here
            # collected_clumpers = []

            # iterate through each path in the glob
            for p in path_list:
                # set the path variable
                bound_arguments.arguments[param_name] = str(p)

                # call the underlying reader function
                clumper = f(*bound_arguments.args, **deepcopy(bound_arguments.kwargs))  # pylint: disable=W0612

                # collect the clumper
                # collected_clumpers.append(clumper)

            # TODO: Not required since load function adds to existing  # pylint: disable=W0511
            # knowledge graph. Delete commented code on confirmation

            # # Only one object found
            # if len(collected_clumpers) == 1:
            #     return collected_clumpers[0]
            # # More than one object found
            # elif len(collected_clumpers) > 1:
            #     # Combine them by concatenating their dict
            #     ic(collected_clumpers)
            #     # return reduce(lambda a, b: a.concat(b), collected_clumpers)

        return wrapper

    return decorator
