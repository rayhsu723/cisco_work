#!/usr/bin/python
"""
    2016-Jul-21 : alway
    Parsing of module paths for 4 architectures: arm, atom_x86, x86_64, bwde_x86
    Output: .csv file
"""
from __future__ import print_function

import os
import re

build_directory = "../../../build"
module_mk_path  = "../../../build/module-path.mk"
arm_mk_path     = "../../../build/diag-lc-arm.mk"
atom_mk_path    = "../../../build/diag-lc-atom.mk"
x86_64_mk_path  = "../../../build/diag-sup-x86_64.mk"
bwde_mk_path    = "../../../build/diag-tor2-bwde_x86.mk"

def parse_module(module_mk_path):
    module_dict = dict()
    with open(module_mk_path) as current_file:
        for line in current_file:
            line = line.strip()
            if line.startswith('ifeq') or line.startswith('else') or line.startswith('endif'):
                continue
            else:
                mod_present = re.search(r"(.+)=\$\(TOP_DIR\)(.+)", line)
                if mod_present:
                    #print("Key: {} Value: {}".format(mod_present.group(1), mod_present.group(2)))
                    mod_key = mod_present.group(1)
                    mod_value = mod_present.group(2)
                    module_dict[mod_key] = mod_value
    return module_dict

def parse_mk(arch):
    arch_dict = dict()
    arch_dict["mk"] = set() #module keys
    arch_dict["dp"] = set() #direct paths
    with open(arch) as current_file:
        for line in current_file:
            line = line.strip()
            if line.startswith('#') or line.startswith('include'):
                continue
            else:
                line = line.partition('#')[0]
                line = line.strip()  #paranoia strip
                if "TOP_DIR" not in line:
                    modkey_present = re.search(r"DIAG_MODULES \+= \$\((.+)\)", line)
                    if modkey_present:
                        #print("diag_mod: {}".format(modkey_present.group(1)))
                        diag_mod = modkey_present.group(1)
                        if diag_mod == "diag_folder5_path" or diag_mod == "diag_sesto_lib_path" or diag_mod == "diag_qsfp_util_path":
                            continue
                        arch_dict["mk"].add(diag_mod)
                elif "TOP_DIR" in line:
                    path_present = re.search(r"DIAG_MODULES \+= \$\(TOP_DIR\)(.+)", line)
                    if path_present:
                        #print("path: {}".format(path_present.group(1)))
                        direct_path = path_present.group(1)
                        arch_dict["dp"].add(direct_path)
    return arch_dict

def generate_main_table(module_dict, arch_dict_list):
    main_table = dict()
    for mod_key, mod_val in module_dict.items():
        if mod_val not in main_table:
            main_table[mod_val] = False
    for a_dict in arch_dict_list:
        for path in a_dict["dp"]:
            if path not in main_table:
                main_table[path] = False
    return main_table

def write_arch_table(main_table, module_dict, arch_dict):
    arch_table = main_table.copy()
    for table_key in main_table:
        if table_key in arch_dict["dp"]:
            arch_table[table_key] = True
        else:
            for mk_key in arch_dict["mk"]:
                path = module_dict[mk_key]
                if table_key == path:
                    arch_table[table_key] = True
    return arch_table

def write_csv_file(main_table, arch_table_list):
    filename = "genarchpath.csv"
    print("Writing csv file: {}".format(filename))
    open(filename, 'w').close()
    f = open(filename, 'ab')
    f.write("Paths,arm,x86_64,atom_x86,bwde_x86\n")
    for path in sorted(main_table.iterkeys()):
        f.write(path)
        for arch_table in arch_table_list:
            if arch_table[path]:
                f.write(",{}".format("X"))
            else:
                f.write(",")
        f.write("\n")
    f.close()
    print("Done.")

def main():
    module_dict   = parse_module(module_mk_path)
    arm_dict      = parse_mk(arm_mk_path)
    x86_64_dict   = parse_mk(x86_64_mk_path)
    atom_dict     = parse_mk(atom_mk_path)
    bwde_dict     = parse_mk(bwde_mk_path)

    arch_dict_list    = [arm_dict, x86_64_dict, atom_dict, bwde_dict]
    main_table    = generate_main_table(module_dict, arch_dict_list)

    arm_table     = write_arch_table(main_table, module_dict, arm_dict)
    x86_64_table  = write_arch_table(main_table, module_dict, x86_64_dict)
    atom_table    = write_arch_table(main_table, module_dict, atom_dict)
    bwde_table    = write_arch_table(main_table, module_dict, bwde_dict)

    arch_table_list = [arm_table, x86_64_table, atom_table, bwde_table]
    write_csv_file(main_table, arch_table_list)

main()
