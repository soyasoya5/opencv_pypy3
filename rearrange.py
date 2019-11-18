#! /usr/bin/env python
import os, sys
import re

class CVType():
    def __init__(self, name, storage, sname, base, constructor):
        self.name = name.strip()
        self.storage = storage.strip()
        self.sname = sname.strip()
        self.base = base.strip()
        self.constructor = constructor.strip()

    def __eq__(self, other):
        return self.name == other.name


def main(argc, argv):
    if argc < 3:
        print("Sorts pyopencv generated macros to initialize base class first")
        print("usage: rearrange.py pyopencv_generated_types.h output_file")
        sys.exit(1)

    in_filename = argv[1]
    out_filename = argv[2]
    edges = build_graph(argv[1])
    sorted_edges = []

    print("Sorting edges")
    sort_edges(edges, sorted_edges)
    # print(sorted_edges)

    print("Writing to file...")
    build_header(edges, sorted_edges, out_filename)

    print("Done..")

def build_graph(infile):
    types = [CVType('NoBase', "", "", "", "")]
    with open(infile, 'r') as f:
        for line in f:
            cv_type = CVType( *(line[10:-3].split(',')) )
            types.append(cv_type)
    
    return types

def sort_edges(class_list, sorted_list):
    for idx, _class in enumerate(class_list):
        add_edge_recursive(_class, class_list, sorted_list)

def add_edge_recursive(_class, class_list, sorted_list):
    if _class.base is not '' and _class.base not in sorted_list:
        add_edge_recursive(find_edge(_class.base, class_list), class_list, sorted_list)

    if _class.name is not 'NoBase' and _class.name not in sorted_list:
        sorted_list.append(_class.name)

def build_header(edges, sorted_edges, outf):
    with open(outf, "w") as f:
        for se in sorted_edges[:]:
            edge = find_edge(se, edges)
            f.write(build_line(edge))

def build_line(edge) :
    return f"CVPY_TYPE({edge.name}, {edge.storage}, {edge.sname}, {edge.base}, {edge.constructor});\n"

def find_edge(name, edges):
    for edge in edges:
        if edge.name == name:
            return edge

    raise Exception(f"Unable to find class {name} in list")

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
