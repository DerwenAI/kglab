#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
## Impl apidoc-ish for actual Markdown: you're welcome.

import inspect
import os
import re
import sys

"""
The PEP proposes adding `frungible doodads`_ to the core.  
It extends PEP 9876 [#pep9876]_ via the BCA [#]_ mechanism.

See also: 

  * [PEP 256](https://www.python.org/dev/peps/pep-0256/)
  * [`inspect`](https://docs.python.org/3/library/inspect.html)

Because there doesn't appear to be any other Markdown-friendly
docstring support in Python.
"""

PAT_PARAM = re.compile(r"(    \S+.*\:\n(?:\S.*\n)+)", re.MULTILINE)
PAT_NAME = re.compile(r"^\s+(.*)\:\n(.*)")
PAT_FWD_REF = re.compile(r"ForwardRef\('(.*)'\)")


def show_all_elements (module_name):
    module_obj = sys.modules[module_name]

    for name, obj in inspect.getmembers(module_obj):
        for n, o in inspect.getmembers(obj):
            print("\n", name, n, o)
            print(type(o))


def fix_fwd_refs (anno):
    """substitute the quoted forward references of module classes"""
    results = []

    if not anno:
        return None
    else:
        for term in anno.split(", "):
            for chunk in PAT_FWD_REF.split(term):
                if len(chunk) > 0:
                    results.append(chunk)

        return ", ".join(results)


def parse_method_docstring (docstring, arg_dict):
    md = []

    for chunk in PAT_PARAM.split(docstring):
        m_param = PAT_PARAM.match(chunk)

        if m_param:
            param = m_param.group()
            m_name = PAT_NAME.match(param)

            if m_name:
                name = m_name.group(1).strip()
                anno = fix_fwd_refs(arg_dict[name])
                descrip = m_name.group(2).strip()

                if name == "returns":
                    md.append("\n  * *{}* : `{}`  \n{}".format(name, anno, descrip))
                elif name == "yields":
                    md.append("\n  * *{}* :  \n{}".format(name, descrip))
                else:
                    md.append("\n  * `{}` : `{}`  \n{}".format(name, anno, descrip))
        else:
            chunk = chunk.strip()

            if len(chunk) > 0:
                md.append(chunk)

    return "\n".join(md)


def extract_type_annotation (sig):
    type_name = str(sig)
    type_class = sig.__class__.__module__

    if type_class != "typing":
        type_name = type_name.split("'")[1]

    if type_name == "~AnyStr":
        type_name = "typing.AnyStr"
    elif type_name.startswith("~"):
        type_name = type_name[1:]

    return type_name


def get_arg_list (sig):
    arg_list = []

    for param in sig.parameters.values():
        #print(param.name, param.empty, param.default, param.annotation, param.kind)

        if param.name == "self":
            pass
        else:
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                name = "*{}".format(param.name)
            elif param.kind == inspect.Parameter.VAR_KEYWORD:
                name = "**{}".format(param.name)
            elif param.default == inspect.Parameter.empty:
                name = param.name
            else:
                if isinstance(param.default, str):
                    default_repr = repr(param.default).replace("'", '"')
                else:
                    default_repr = param.default

                name = "{}={}".format(param.name, default_repr)

            anno = extract_type_annotation(param.annotation)
            arg_list.append((name, anno))

    return arg_list


def append_doc (md, obj, parse=False, arg_dict={}):
    doc = obj.__doc__

    if doc:
        docstring = inspect.cleandoc(doc)

        if parse:
            md.append(parse_method_docstring(docstring, arg_dict))
        else:
            md.append(docstring)

        md.append("\n")


def document_method (path_list, name, obj, func_kind, gh_src_url):
    md = ["---"]

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
    arg_list_str = "{}".format(", ".join([ a[0] for a in arg_list ]))

    md.append("```python")
    md.append("{}({})".format(name, arg_list_str))
    md.append("```")

    # include the docstring, with return annotation
    arg_dict = dict([ (name.split("=")[0], anno,) for name, anno in arg_list ])
    arg_dict["yields"] = None

    ret = sig.return_annotation

    if ret:
        arg_dict["returns"] = extract_type_annotation(ret)

    append_doc(md, obj, parse=True, arg_dict=arg_dict)
    md.append("")

    return line_num, md


def document_type (path_list, name, obj):
    md = []

    # format a header + anchor
    frag = ".".join(path_list + [ name ])
    anchor = "#### [`{}` {}](#{})".format(name, "type", frag)
    md.append(anchor)

    # show type definition
    md.append("```python")
    md.append("{} = {}".format(name, obj))
    md.append("```")
    md.append("")

    return md


def write_markdown (filename):
    with open(filename, "w") as f:
        for line in md:
            f.write(line)
            f.write("\n")


if __name__ == "__main__":
    ref_md_file = sys.argv[1]
    class_list = [ "KnowledgeGraph", "Measure", "Simplex0", "Simplex1", "Subgraph" ]

    ## NB: `inspect` is picky about paths and current working directory
    ## this only works if run from the top-level directory for the repo

    sys.path.insert(0, "../")
    import kglab

    module_name = "kglab"
    module_obj = sys.modules[module_name]
    gh_src_url = "https://github.com/DerwenAI/kglab/blob/main"

    ## NB: uncomment to analyze/troubleshoot the results of `inspect` 
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

        doc = class_obj.__doc__

        if doc:
            md.append(doc)

        obj_md_pos = {}

        for member_name, member_obj in inspect.getmembers(class_obj):
            path_list = [module_name, class_name]

            if member_name.startswith("__") or not member_name.startswith("_"):
                if inspect.isfunction(member_obj):
                    func_kind = "method"
                elif inspect.ismethod(member_obj):
                    func_kind = "classmethod"
                else:
                    continue

                line_num, obj_md = document_method(path_list, member_name, member_obj, func_kind, gh_src_url)
                obj_md_pos[line_num] = obj_md

        for pos, obj_md in sorted(obj_md_pos.items()):
            md.extend(obj_md)

    ## walk the module tree for each function definition
    md.append("---")
    md.append("## [module functions](#{})".format(module_name, "functions"))

    for func_name, func_obj in inspect.getmembers(module_obj, inspect.isfunction):
        if not func_name.startswith("_"):
            line_num, obj_md = document_method([module_name], func_name, func_obj, "function", gh_src_url)
            md.extend(obj_md)

    # walk the list of types in the module
    md.append("---")
    md.append("## [module types](#{})".format(module_name, "types"))

    for name, obj in inspect.getmembers(module_obj):
        if obj.__class__.__module__ == "typing":
            if not str(obj).startswith("~"):
                obj_md = document_type([module_name], name, obj)
                md.extend(obj_md)

    ## output markdown
    print("writing: ", ref_md_file)
    write_markdown(ref_md_file)
