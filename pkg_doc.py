#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
## Impl apidoc-ish for actual Markdown: you're welcome.

import inspect
import os
import sys

"""
This PEP proposes adding `frungible doodads`_ to the core.  
It extends PEP 9876 [#pep9876]_ via the BCA [#]_ mechanism.

See also: 

  * [PEP 256](https://www.python.org/dev/peps/pep-0256/)
  * [`inspect`](https://docs.python.org/3/library/inspect.html)

Because there doesn't appear to be any other Markdown-friendly
docstring support in Python.
"""


def show_all_elements (module_name):
    module_obj = sys.modules[module_name]

    for name, obj in inspect.getmembers(module_obj, inspect.isclass):
        for n, o in inspect.getmembers(obj):
            print("\n", name, n, o)
            print(type(o))


def get_arg_list (sig):
    arg_list = []

    for param in sig.parameters.values():
        #print(param.name, param.empty, param.default, param.annotation, param.kind)

        if param.name == "self":
            pass
        elif param.kind == inspect.Parameter.VAR_POSITIONAL:
            arg_list.append("*{}".format(param.name))
        elif param.kind == inspect.Parameter.VAR_KEYWORD:
            arg_list.append("**{}".format(param.name))
        elif param.default == inspect.Parameter.empty:
            arg_list.append(param.name)
        else:
            if isinstance(param.default, str):
                default_repr = repr(param.default).replace("'", '"')
            else:
                default_repr = param.default

            arg_list.append("{}={}".format(param.name, default_repr))

    return arg_list


def append_doc (md, obj):
    doc = obj.__doc__

    if doc:
        md.append(inspect.cleandoc(doc))
        md.append("\n")


def document_method (path_list, name, obj, func_kind, gh_src_url):
    md = []

    # format a header + anchor
    frag = ".".join(path_list + [ name ])
    anchor = "#### [`{}` {}](#{})".format(name, func_kind, frag)
    md.append(anchor)

    # link to source code in Git repo
    code = obj.__code__
    line_num = code.co_firstlineno
    file = code.co_filename.replace(os.getcwd(), "")
    src_url = "[*\[source\]*]({}{}#L{})\n".format(gh_src_url, file, line_num)
    md.append(src_url)

    # format the callable signature
    sig = inspect.signature(obj)
    arg_list = get_arg_list(sig)
    arg_list_str = "{}".format(", ".join(arg_list))

    md.append("```python")
    md.append("{}({})".format(name, arg_list_str))
    md.append("```")

    # include the docstring
    append_doc(md, obj)

    # format the return annotation
    ret = sig.return_annotation

    if ret:
        ret_name = str(ret)
        ret_class = ret.__class__.__module__

        if ret_class != "typing":
            ret_name = ret_name.split("'")[1]

        md.append("*returns:* `{}`".format(ret_name))

    md.append("")

    return line_num, md


def write_markdown (filename):
    with open(filename, "w") as f:
        for line in md:
            f.write(line)
            f.write("\n")


if __name__ == "__main__":
    ref_md_file = sys.argv[1]
    class_list = [ "KnowledgeGraph", "Measure", "Simplex0", "Simplex1", "Subgraph" ]

    import kglab
    module_name = "kglab"
    module_obj = sys.modules[module_name]
    gh_src_url = "https://github.com/DerwenAI/kglab/blob/main"

    #show_all_elements(module_name)
    #sys.exit(0)

    ## format markdown
    todo_list = {}
    md = []

    md.append("# Reference: `{}` package".format(module_name))
    append_doc(md, module_obj)

    ## walk the module tree to find class definitions
    for class_name, class_obj in inspect.getmembers(module_obj, inspect.isclass):
        if class_name in class_list:
            todo_list[class_name] = class_obj

    ## format each specified class definition
    for class_name in class_list:
        class_obj = todo_list[class_name]

        md.append("## [`{}` class](#{})".format(class_name, class_name))
        obj_md_pos = {}

        for member_name, member_obj in inspect.getmembers(class_obj):
            path_list = [module_name, class_name]

            if inspect.isfunction(member_obj):
                line_num, obj_md = document_method(path_list, member_name, member_obj, "method", gh_src_url)
                obj_md_pos[line_num] = obj_md
            elif inspect.ismethod(member_obj):
                line_num, obj_md = document_method(path_list, member_name, member_obj, "classmethod", gh_src_url)
                obj_md_pos[line_num] = obj_md

        for pos, obj_md in sorted(obj_md_pos.items()):
            md.extend(obj_md)

    ## walk the module tree for each function definition
    md.append("---")
    md.append("## [module functions](#{})".format(module_name, "functions"))

    for func_name, func_obj in inspect.getmembers(module_obj, inspect.isfunction):
        line_num, obj_md = document_method([module_name], func_name, func_obj, "function", gh_src_url)
        md.extend(obj_md)

    ## output markdown
    print("writing: ", ref_md_file)
    write_markdown(ref_md_file)
