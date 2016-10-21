#!/usr/bin/python

import os
import re
import subprocess
import yaml

""" 1) Checks for tests/commands from c files that are missing in the yaml files (and vice versa). 
    2) Also checks to make sure they have the same DSPs. If not, it has been added to the exceptions list.

    3) Based on the parameters in the .cpp code, this program checks which 
       parameters are missing from the commands/tests already present in the yaml files. """

FLAGS_DSP_EXCEPTIONS_C       = ["TD2", "ASIC", "EXAMPLE", "dispatcher"]  # dsp names found in c files but not in yaml files
FLAGS_DSP_EXCEPTIONS_Y       = ["TRF"]                                   # dsp names found in yaml files but not in c files
DSP_DIRECTORY_EXCEPTIONS_C   = ["mpa_qsfp", "dispatcher", "example"]     # dsp directories to be ignored for parsing in generate_c_dict()
CMD_EXCEPTIONS               = ["dummy-cmd", "dummy_cmd", "dummy"]       # commands to be ignored from both c and yaml files

# Compiles all tests/cmds present in the yaml files into a dictionary. (exclude run_cnt and timeout) 
# The dictionary is formatted as Key: <DSP> Value: set(<test/cmd 1>, <test/cmd 2>,...., <test/cmd n>)
def generate_yaml_dict():
	yaml_dict = dict()
	test_set = set()
	yaml_directory = "../dspYaml"

	for filename in os.listdir(yaml_directory):
		if filename == "warnings.txt" or filename.endswith("~"):
			continue
		filepath = yaml_directory + '/' + filename
		y = yaml.safe_load(open(filepath, 'r'))
		if "n3k" in filename:
			DSP_name = "N3K" + y['DSP']['NAME']
		else:
			DSP_name = y['DSP']['NAME']

		for key in y:
			if key == 'DSP':
				continue
			else:
				test_name = key.split('#')
				test_set.add(test_name[1])

		yaml_dict[DSP_name] = test_set

		# reset test_set
		test_set = set()

	return yaml_dict

# Helper for generate_c_dict(). Returns the dsp_names for the specified diagsp.cpp file

def get_dsp_name(diagsp_file_path):
 	grep_call = subprocess.Popen(['grep', '-rsI', 'FLAGS_dsp =', diagsp_file_path], stdout = subprocess.PIPE)
 	grep_output = grep_call.stdout.read().splitlines()
 	dsp_name_set = set()
 	for grep_line in grep_output:
 		dsp_flag_exists = re.search('FLAGS_dsp = \"(.+)\";', grep_line)
 		if dsp_flag_exists:
 			dsp_name = dsp_flag_exists.group(1)
 			if dsp_name not in FLAGS_DSP_EXCEPTIONS_C:
 				dsp_name_set.add(dsp_name)
 	return dsp_name_set

# Helper for generate_c_dict(). Returns a set of tests/cmds corresponding to the given dsp

# def get_testcmd_set(diagsp_file_path):
# 	grep_call = subprocess.Popen(['grep', '-rsI', '_TEST_HDL_MAP_', diagsp_file_path], stdout = subprocess.PIPE)
# 	grep_output = grep_call.stdout.read().splitlines()
# 	testcmd_set = set()
# 	for grep_line in grep_output:
# 		test_handler_exists = re.search('\s+_TEST_HDL_MAP_\[(\s*)\"(.+)\"(\s*)\](\s*)=(\s*)&(.+);', grep_line)
# 		if test_handler_exists:
# 			testcmd = test_handler_exists.group(2)
# 			if testcmd not in CMD_EXCEPTIONS:
# 				testcmd_set.add(testcmd)
# 	return testcmd_set

# Returns a dictionary Key: <DSP> Value: <set of tests/cmds>
def generate_c_dict():
	c_dict = dict()
	test_set = set()
	dsp_directory = "../../../../dsp"
	for directory in os.listdir(dsp_directory):
		if directory in DSP_DIRECTORY_EXCEPTIONS_C:
			continue


		if directory == "tomahawk" or directory == "trident":
			grep_path = '../../../../../../../sdk-xgs-robo-6.4.8/src/customer/trident_diagsp.cpp'
			grep_call = subprocess.Popen(['grep', '-rsnI', '_TEST_HDL_MAP_', grep_path], stdout = subprocess.PIPE)
			grep_output = grep_call.stdout.readlines()

			for grep_line in grep_output:
				get_test_name = re.search('(\d*):(\s*)_TEST_HDL_MAP_\["(.*)"\]\s+=\s+&(.*);' , grep_line)
				if get_test_name == None:
					continue
				else:
					test_set.add(get_test_name.group(3))
			c_dict[directory.upper()] = test_set
			test_set = set()



		elif directory == "mvl10port" or directory == "mvl4port":
			grep_path = '../../../../dsp/mvl4port/mvl4port_diagsp.cpp'
			grep_call = subprocess.Popen(['grep', '-rsnI', '_TEST_HDL_MAP_', grep_path], stdout = subprocess.PIPE)
			grep_output = grep_call.stdout.readlines()

			for grep_line in grep_output:
				get_test_name = re.search('(\d*):(\s*)_TEST_HDL_MAP_\["(.*)"\]\s+=\s+&(.*);' , grep_line)
				get_prefix_test_name = re.search('(\d*):(\s*)_TEST_HDL_MAP_\[prefix\+"(.*)"]\s+=\s+&(.*);', grep_line)
				if get_test_name == None:
					pass
				elif (get_test_name.group(3) == "EPC_SC1" or get_test_name.group(3) == "EPC_SC2"):
					if directory == "mvl10port":
						test_set.add(get_test_name.group(3))
				else:
					test_set.add(get_test_name.group(3))
				if get_prefix_test_name == None:
					continue
				else:
					test_set.add(directory + get_prefix_test_name.group(3))
			c_dict[directory[:-3].upper()] = test_set
			test_set = set()



		else:
			grep_path = dsp_directory + "/" + directory
			grep_call = subprocess.Popen(['grep','-rsnI', "_TEST_HDL_MAP_", grep_path], stdout = subprocess.PIPE)
			grep_output = grep_call.stdout.readlines()

			for grep_line in grep_output:
					get_test_name = re.search('(.*):(\d*):(\s*)_TEST_HDL_MAP_\["(.*)"\]\s+=\s+&(.*);' , grep_line)
					if get_test_name == None:
						continue
					else:
						test_set.add(get_test_name.group(4))
			if directory == "lacrosse":
				c_dict['LAX'] = test_set
			elif directory == "boreal":
				c_dict["BOR"] = test_set
			elif directory == "brcm28port":
				c_dict["BRCM28P"] = test_set
			elif directory == 'mpa_misc':
				c_dict["MISC_MPA"] = test_set
			elif directory == "n3kmux":
				c_dict['N3KMUX'] = test_set
			elif directory == "n3kbrd":
				c_dict['N3KMISC'] = test_set
			else:
				c_dict[directory.upper()] = test_set

			test_set = set()



	#handle simple exceptions
	alpine_test_set = c_dict["NORTHSTAR"].union(c_dict["ALPINE"])
	c_dict.pop("ALPINE", None)
	c_dict["ALPINE"] = alpine_test_set

	ge_test_set = c_dict["MVL_GE_PHY"].union(c_dict["BCM_GE_PHY"])
	c_dict.pop("MVL_GE_PHY", None)
	c_dict.pop("BCM_GE_PHY", None)
	c_dict["GE"] = ge_test_set

	return c_dict

# Checks that the same DSPs are present in both dictionaries
def dsp_check(yaml_dict, c_dict):

	pass_check = True
	if len(yaml_dict) != len(c_dict):
		pass_check = False
		print "dsp_check error: yaml_dict length ({}) does not match c_dict length ({})".format(len(yaml_dict), len(c_dict))
	for ykey in yaml_dict:
		found = False
		for ckey in c_dict:
			if ckey == ykey:
				found = True
		if not found:
			pass_check = False
			print "dsp_check error: {} is missing from c_dict".format(ykey)
	for ckey in c_dict:
		found = False
		for ykey in yaml_dict:
			if ckey == ykey:
				found = True
		if not found:
			pass_check = False
			print "dsp_check error: {} is missing from yaml_dict".format(ykey)
	if pass_check:
		print "dsp_check PASSED"
	else:
		print "dsp_check FAILED"

def merge_dsp_dict(yaml_dict, c_dict):
	merged_dict = dict()
	for key, value in yaml_dict.items():
		if key not in c_dict.keys():
			continue
		else:
			merged_dict[key] = yaml_dict[key] & c_dict[key]
	return merged_dict

# Checks which tests/cmds are missing from yaml_dict or c_dict
#def merge_dict(yaml_dict, c_dict):
#	merged_dict = dict()
#	for dsp_name, y_set in yaml_dict.items():
#		new_set = yaml_dict[dsp_name].intersection(c_dict[dsp_name])
#		merged_dict[dsp_name] = new_set
#	return merged_dict


def testcmd_check(yaml_dict, c_dict, merged_dict):
	pass_check = True

	open('yaml_missing_testscmds.log', 'w').close()
	open('c_missing_testscmds.log', 'w').close()

	fy = open('yaml_missing_testscmds.log','ab')
	fc = open('c_missing_testscmds.log','ab')

	missing_in_yaml = []
	missing_in_c = []

	merged_keys = merged_dict.keys()
	merged_keys.sort()
	for c_keys, c_set in c_dict.items():
		if c_keys not in merged_keys:
			continue
		else:
			for testcmd in c_set:
				if testcmd not in merged_dict[c_keys]:
					missing_testcmd = c_keys + ":" + testcmd
					missing_in_yaml.append(missing_testcmd)
					pass_check = False

	for y_keys, y_set in yaml_dict.items():
		if y_keys not in merged_keys:
			continue
		else:
			for testcmd in y_set:
				if testcmd not in merged_dict[y_keys]:
					missing_testcmd = y_keys + ":" + testcmd
					missing_in_c.append(missing_testcmd)
					pass_check = False

	for testcmd in missing_in_yaml:
		fy.write("%30s is missing from yaml file\n" % (testcmd))
	for testcmd in missing_in_c:
		fc.write("%30s is missing from c file\n" % (testcmd))
	if pass_check:
		print "testcmd_check PASSED"
	else:
		print "testcmd_check FAILED"
	fy.close()
	fc.close()



# Returns dictionary of Key: <DSP:test/cmd> Value: <set of params>
def generate_yaml_param_dict():
	yaml_param_dict = dict()
	param_set = set()
	yaml_directory = "../dspYaml"

	for filename in os.listdir(yaml_directory):
		if filename == "warnings.txt" or filename.endswith("~"):
			continue
		filepath = yaml_directory + '/' + filename
		y = yaml.safe_load(open(filepath, 'r'))
		if "n3k" in filename:
			DSP_name = "N3K" + y['DSP']['NAME']
		else:
			DSP_name = y['DSP']['NAME']

		for key in y:
			if key == "DSP":
				continue
			else:
				test_name = key.split('#')

				for param_key in y[key]:
					if param_key == "PARAM":
						for param in y[key][param_key]:
							if "run_cnt" in param or "timeout" in param:
								continue
							param_name = param.split('@')
							param_set.add(param_name[0])
			dict_key = DSP_name + ":" + test_name[1]
			yaml_param_dict[dict_key] = param_set
			param_set = set()
			
	return yaml_param_dict

# Creates dictionary of Key: <DSP> Value:<(diagsp path, dsp directory path)>
def generate_dsp_diagsppath_map():
	dsp_diagsppath_map = dict() # Key: <dsp> Value: <diagsp path>
	c_directory = "../../../../dsp"
	# Generate keys first

	dsp_diagsppath_map['N3KMISC'] = ("../../../../dsp/n3kbrd/n3kbrd_diagsp.cpp", "../../../../dsp/n3kbrd")
	dsp_diagsppath_map["N3KMUX"] = ("../../../../dsp/n3kmux/n3kmux_diagsp.cpp", "../../../../dsp/n3kmux")

	for dsp_directory in os.listdir(c_directory):
		if dsp_directory in DSP_DIRECTORY_EXCEPTIONS_C:
			continue
		if dsp_directory == "n3kmux" or dsp_directory == "n3kbrd":
			continue
		dsp_directory = c_directory + "/" + dsp_directory
		# Find the _diagsp.cpp file in each dsp directory
		for filename in os.listdir(dsp_directory):
			# Skip hidden files
			if filename.endswith("~"):
				continue
			diagsp_exists = re.search('(.+_diagsp.cpp)', filename)
			if diagsp_exists:
				diagsp_file_path = dsp_directory + "/" + diagsp_exists.group(1)
				dsp_name_set = get_dsp_name(diagsp_file_path)
				for dsp_name in dsp_name_set:
					if dsp_name not in dsp_diagsppath_map:
						if dsp_name == "ALPINE" or dsp_name == "GE" or dsp_name == "MVL10P":
							dsp_diagsppath_map[dsp_name] = set()
							dsp_diagsppath_map[dsp_name].add((diagsp_file_path, dsp_directory))
						elif dsp_name == "TRIDENT":
							dsp_diagsppath_map['TRIDENT'] = ("../../../../../../../sdk-xgs-robo-6.4.8/src/customer/trident_diagsp.cpp", "../../../../../../../sdk-xgs-robo-6.4.8/src/customer")
							dsp_diagsppath_map['TOMAHAWK'] = ("../../../../../../../sdk-xgs-robo-6.4.8/src/customer/trident_diagsp.cpp", "../../../../../../../sdk-xgs-robo-6.4.8/src/customer")
						else:
							dsp_diagsppath_map[dsp_name] = (diagsp_file_path, dsp_directory)
					elif dsp_name == "ALPINE" or dsp_name == "GE" or dsp_name == "MVL10P":
							dsp_diagsppath_map[dsp_name].add((diagsp_file_path, dsp_directory))
	return dsp_diagsppath_map

# Helper function for generate_c_param_dict. Returns the function handler for a given test/cmd
def get_functname_set(diagsp_file_path, test_cmd):

	grep_call = subprocess.Popen(['grep', '-swI', test_cmd, diagsp_file_path], stdout = subprocess.PIPE)
	grep_output = grep_call.stdout.read().splitlines()
	if grep_output == []:
		return None
	functname_set = set()
	for grep_line in grep_output:
		funct_exists = re.search('\s+_TEST_HDL_MAP_\[(\s*)\"' + test_cmd + '\"(\s*)\](\s*)=(\s*)&(.+?);(.*)', grep_line)
		
		if funct_exists:
		 	functname_set.add(funct_exists.group(5))
	return functname_set

# Helper function for generate_c_param_dict. 
# Returns a set where each element is (cpp_path, line_num, funct_line) of the given function handler
def get_cpp_file_set(dsp_directory, functname_set):

	cpp_file_set = set()
	GREP_EXCEPTIONS = ["extern", "_TEST_HDL_MAP_", ";", "//", "*", "!="]
	for funct_name in functname_set:
		grep_call = subprocess.Popen(['grep', '-rswnI', '--exclude=*.h', funct_name, dsp_directory], stdout = subprocess.PIPE)
		grep_output = grep_call.stdout.read().splitlines()
		if grep_output == []:
			print "CPP_FILE_SET GREP_CALL ERROR: " + dsp_directory
			return None
		for grep_line in grep_output:
			if any(g_ex in grep_line for g_ex in GREP_EXCEPTIONS):
				continue
			funct_line_exists = re.search('(.*):(\d+):(.*)', grep_line)
			if funct_line_exists:
				cpp_path = funct_line_exists.group(1)
				line_num = funct_line_exists.group(2)
				funct_line = funct_line_exists.group(3)
				cpp_file_set.add((cpp_path, line_num, funct_line))
	return cpp_file_set

# Helper function for get_c_params.
# Returns the a set of (param, type, value) from given param_set
def get_param_typval(cpp_path, param_set):
	# Set of three element tuples (param, type, value)
	new_param_set = set()
	with open(cpp_path) as current_file:
		for line in current_file:
			for param in param_set:
				if param in line and ("DEFINE_" in line or "DECLARE_" in line):
					line.strip()
					param_parts = re.search(r"DEFINE_(.+?)\((|.+?),\s+(\"?.+?\"?),.*", line)
					if param_parts:
						if param != param_parts.group(2):
							continue
						param_type = param_parts.group(1)
						param_val = param_parts.group(3)
						# (param, type, value)
						new_param_set.add((param, param_type, param_val))					
	return new_param_set

# Helper function for generate_c_param_dict.
# Returns 
def get_c_params(cpp_file_set):
	param_set = set()
	# Check each cpp file in the set. This is for ONE test/cmd
	# param_set is the master set. Each cpp file has its own param_subset
	# we add param_subset to param_set at the end of each loop iteration
	if cpp_file_set == None:
		return param_set
	for c in cpp_file_set:
		param_subset = set()
		cpp_path = c[0]
		line_num = c[1]
		funct_line = c[2]
		with open(cpp_path) as current_file:
			for i in xrange(int(line_num)-1):
					current_file.next()
			bracket_count = 0
			first_bracket = True
			for line in current_file:
				if "{" in line:
					first_bracket = False
					bracket_count += 1
				if "}" in line:
					bracket_count -= 1
				if "FLAGS_" in line:
					string_list = re.findall(r"[_|\w']+", line)
					# Parse FLAGS_<param>
					for s in string_list:
						if "FLAGS_" in s:
							param = re.sub("FLAGS_","",s,count=1)
							param_subset.add(param)
				if bracket_count == 0 and not first_bracket:
					break
		param_subset_final = get_param_typval(cpp_path, param_subset)
		param_set = param_set.union(param_subset_final)
	return param_set 

# Key: <DSP:TEST/CMD> Value: <set of param tuples(param, type, value)>
def generate_c_param_dict(dsp_diagsppath_map, merged_dict):
	c_param_dict = dict()
	for dsp_name, diagsp_path in dsp_diagsppath_map.items():
		if dsp_name not in merged_dict.keys():
			continue	
		for test_cmd in merged_dict[dsp_name]:
			if dsp_name == "ALPINE" or dsp_name == "GE" or dsp_name == "MVL10P":
				for path in diagsp_path:
					functname_set = get_functname_set(path[0], test_cmd)
					if not functname_set:
						continue
					cpp_file_set = get_cpp_file_set(path[1], functname_set)
					param_set = get_c_params(cpp_file_set)
					new_key = dsp_name + ":" + test_cmd
					c_param_dict[new_key] = param_set
					break
			else:	
				functname_set = get_functname_set(diagsp_path[0], test_cmd)
				if not functname_set:
					print "Error: functname empty for {}:{}".format(dsp_name, test_cmd)
				cpp_file_set = get_cpp_file_set(diagsp_path[1], functname_set)
				if not cpp_file_set:
					print "Error: cpp_file_set empty for {}:{}".format(dsp_name, test_cmd)
				param_set = get_c_params(cpp_file_set)
				new_key = dsp_name + ":" + test_cmd
				c_param_dict[new_key] = param_set
	return c_param_dict

def find_missing_params(yaml_param_dict, c_param_dict, merged_dict):
	open('yaml_missing_params.log', 'w').close()
	f = open('yaml_missing_params.log', 'ab')

	for dsp_name in sorted(merged_dict.iterkeys()):
		something_off = False
		for test_cmd in sorted(merged_dict[dsp_name]):
			square_up = False
			if "N3K" in dsp_name:
				master_key = dsp_name[3:] + ":" + test_cmd
			else:
				master_key = dsp_name + ":" + test_cmd
			if master_key not in c_param_dict:
				continue
			c_param_set = c_param_dict[master_key]
			yaml_param_set = yaml_param_dict[master_key]
			for param in c_param_set:
				if param[0] not in yaml_param_set:
					something_off = True
					square_up = True
					left_col = "{}:{}:{}".format(dsp_name, test_cmd, param[0])
					mid_col = "{}: {}".format("type", param[1])
					f.write("{0:<47} {1:<20} value: {2:<20}\n".format(left_col, mid_col, param[2]))
			if square_up:
				f.write("\n")
		if something_off:
			f.write("====================================================================================\n")
			f.write("\n")
	f.close()

def pretty(d, indent=0):
   for key, value in d.iteritems():
      print '\t' * indent + str(key)
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print '\t' * (indent+1) + str(value)


def main():
	# Produce yaml/c dicts and run initial checks
	print("Building yaml_dict..."),
	yaml_dict = generate_yaml_dict()

	print "DONE"
	print("Building c_dict..."),
	c_dict = generate_c_dict()
	#print(sorted(c_dict.keys()))
	print "DONE"
	dsp_check(yaml_dict, c_dict)
	merged_dsp_dict = merge_dsp_dict(yaml_dict, c_dict)

	testcmd_check(yaml_dict, c_dict, merged_dsp_dict)

	# Contains only tests/cmds present in both yaml and c files 
	#merged_dict = merge_dict(yaml_dict, c_dict)

	# Produce yaml/c param dicts
	print("Building yaml_param_dict..."),
	yaml_param_dict = generate_yaml_param_dict()
	print "DONE"
	print("Building diagsp map..."),
	dsp_diagsppath_map = generate_dsp_diagsppath_map()
	print "DONE"
	print("Building c_param_dict..."),
	c_param_dict = generate_c_param_dict(dsp_diagsppath_map, merged_dsp_dict)
	print "DONE"
	print("Finding missing params..."),
	find_missing_params(yaml_param_dict, c_param_dict, merged_dsp_dict)
	print "DONE"

main()
