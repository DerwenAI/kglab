from functools import wraps, reduce
from copy import deepcopy
import inspect
from glob import glob
from pathlib import Path

# decorator to handle multiple paths
def multifile(param_name="path"):
    """
    Creates a wrapper around read function to read multiple file given a pattern with at least one * in the path.
    """

    def decorator(f):
        sig = inspect.signature(f)
        if param_name not in sig.parameters:
            raise ValueError(
                f"Reader function {f.__name__} has no parameter '{param_name}'"
            )

        @wraps(f)
        def wrapper(*args, **kwargs):
            bound_arguments = sig.bind(*args, **kwargs)

            bound_arguments.apply_defaults()

            path = bound_arguments.arguments[param_name]

            # If * not in path then let the default function handle it.
            # We are only interested if the path has * in it
            if isinstance(path, str):
                if "*" not in path:
                    return f(*args, **kwargs)
                else:
                    # Else, create a glob out of it
                    path_list = glob(path)

            # Let default function handle single Path objects
            elif isinstance(path, Path):
                return f(*args, **kwargs)

            # Handle a list of Path objects
            elif isinstance(path, (list)):
                path_list = []
                for p in path:
                    if isinstance(p, Path):
                        path_list.append(p)
                    else:
                        raise ValueError(f"Invalid path: {p}")
            else:
                raise ValueError(
                    f"{path} is not a valid string, Path, or list of Paths"
                )

            # No files found given the pattern so raise error
            if len(path_list) == 0:
                raise ValueError(f"No files found given pattern : {path}")

            # Store the parsed clumpers here
            # collected_clumpers = []

            # Iterate each path in the glob
            for p in path_list:
                # Set the path variable
                bound_arguments.arguments[param_name] = str(p)
                # Call the underlying reader function
                clumper = f(*bound_arguments.args, **deepcopy(bound_arguments.kwargs))
                # Collect the clumper
                # collected_clumpers.append(clumper)

            # TODO: Not required since load function adds to existing knowlege graph. Delete commented code on confirmation
            # # Only one object found
            # if len(collected_clumpers) == 1:
            #     return collected_clumpers[0]
            # # More than one object found
            # elif len(collected_clumpers) > 1:
            #     # Combine them by concating their dict
            #     ic(collected_clumpers)
            #     # return reduce(lambda a, b: a.concat(b), collected_clumpers)

        return wrapper

    return decorator
