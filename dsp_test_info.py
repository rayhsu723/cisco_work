# 2016-AUG-25 : raymhsu
# Creates an xml file that lists all the dsps for a particular board
# script format: python list_dsp_tests.py <board_name>
# return file  : <BOARD_NAME>_dsp.xml

import os
import string
from collections import defaultdict
import subprocess
import sys
import yaml
import re

EXCEPTIONS = ['GE', 'MVL10P', 'MVL4P', 'TRIDENT', 'TOMAHAWK']
# name of board typed converted to all caps
board_name = sys.argv[1].upper()

# path to directory containing all yaml files for dsp
dsp_yaml_path = './dspYaml'


# main_dict has the following format 
#
# {DSP : {
#		   test_name : {	
#							'HELP_INFO' : <str> 
#							'PARAM'     : { name : <str>
#											value : <str> or <int> or whatever }
#						}					
#
#		  }
#}
main_dict = defaultdict(dict)

# yaml_test_param has the following format
# {DSP : {test_name : {param_name : param_info } } }
yaml_test_param = defaultdict(lambda: defaultdict(dict))

# path assumes that file is placed in insdiag/diag/scripts/target_scripts/new_preload
dsp_yaml_path = './dspYaml'

# opens up .config.all.yaml and returns the dictionary
def get_yaml_table():
	y = yaml.safe_load(open("config.yaml", 'r'))
	return y

# takes in a board name and the dictionary from .config.all.yaml and returns string of platform type of board (ex. TOR, FM, LC)
# returns ERROR if board is not any of these types return False
def valid_board(board_name, y):
	# board_name = sys.argv[1]
	if board_name in y['PLATFORM']['TOR']:
		return "TOR"
	elif board_name in y['PLATFORM']['TOR_MPA']:
		return "TOR_MPA"
	elif board_name in y['PLATFORM']['LC']:
		return "LC"
	elif board_name in y['PLATFORM']['FM']:
		return "FM"
	elif board_name in y['PLATFORM']['SC']:
		return "SC"
	elif board_name in y['PLATFORM']['SUP']:
		return "SUP"
	elif board_name in y['PLATFORM']['COR']:
		return "COR"
	elif board_name in y['PLATFORM']['REDII']:
		return "REDII"
	elif board_name in y['PLATFORM']['NKKK']:
		return 'NKKK'
	else:
		return "ERROR"

# checks to see if the file is a <dsp>.tests.yaml file
# also checks to see if there is a corresponding dsp directory for that file; if not, return False

def valid_file(filename):
	filename_list = filename.split('.')
	if filename_list[0][4:] == "eobc":
		return False
	elif (filename_list[0][4:].upper() == "TRIDENT" and filename_list[1] == "tests") or (filename_list[0][4:].upper() == "TOMAHAWK" and filename_list[1] == 'tests'):
		return True
	elif (filename_list[0][4:].upper() == "GE" and filename_list[1] == "tests"):
		return True
    	elif (filename_list[0][4:] == "mvl4p" or filename_list[0][4:] == "mvl10p") and (filename_list[1] == "tests"):
            return True
	elif filename_list[0][4:] not in os.listdir('../../../dsp'):
		return False
	elif filename_list[1] == "tests":
		return True
	else:
		return False

# get the path to the corresponding diag/dsp/ directory

def _get_dsp_path(dsp_name):
    # current path/ -> .. * till you reach diag/ -> dsp_name
    if dsp_name == 'LAX':
	dsp_path = '../../../dsp/lacrosse'
    else:
    	dsp_path = '../../../dsp/' + dsp_name.lower()
    return dsp_path

# helper function that uses regular expression to get DSP test name and the function that is called by that test

def search_test_function(dsp_path, test_name): # dsp path will be the path to the directory containing the _diagsp.cpp file containing all the tests
    test_grep = "_TEST_HDL_MAP_\[\"" + str(test_name) + "\"\]" # prep test name for grep call format
    grep_call = subprocess.Popen(['grep', '-rsnI', test_grep, dsp_path], stdout = subprocess.PIPE)
    grep_output = grep_call.stdout.read()
    func_line_exists = re.search( '(.*):(\d*):(.*)_TEST_HDL_MAP_\["(.*)"\]\s+=\s+&(.*);' , grep_output)
    return func_line_exists.group(5)

# return the cpp file in which the function is included in

def get_func_cpp(func_test, dsp_path):
    grep_call = subprocess.Popen(['grep', '-rsnI', '--exclude=*.h', '--exclude=*diagsp.cpp', str(func_test), str(dsp_path)], stdout = subprocess.PIPE)
    grep_output = grep_call.stdout.readlines()

    for grep_line in grep_output:
            get_cpp_file = re.search('..\/..\/..\/dsp\/\w*\/(.*):(\d*):(\s*)(\w+)(\s+)(.*)\(', grep_line)
            if get_cpp_file == None:
                    continue
            else:
                    return get_cpp_file.group(1)
                    break



# loads yaml_test_param with the info of all the params

def _search_func_file(dsp_name, dsp_path, test_name, cpp_name):
    global yaml_test_param

    real_path = dsp_path + '/' + str(cpp_name) # dsp_path + the name of the cpp file
    grep_call = subprocess.Popen(['grep', '-rsnI', 'DEFINE_', real_path], stdout = subprocess.PIPE)
    grep_output = grep_call.stdout.readlines()
    for p in main_dict[dsp_name][test_name]['PARAM'].keys():
            for grep_line in grep_output:
                    exists = re.search('(\d+):DEFINE_(\w*)\((\w*), (.*), \"(.*)\"\);', grep_line)
                    #exists = re.search('(\d+):DEFINE_(\w*)\((\w*), (.*), (.*)\);', grep_line)
                    if exists == None:
                            continue
                    else:
                            if exists.group(3) == p.lower():
                                    yaml_test_param[dsp_name][test_name][p] = exists.group(5)
                            else:
                                    continue

def _search_func_file_mvlp(dsp_name, test_name, param_name, cpp_path):
        global yaml_test_param
        grep_call =subprocess.Popen(['grep', '-rsnI', 'DEFINE_', cpp_path], stdout = subprocess.PIPE)
        grep_output = grep_call.stdout.readlines()

        for grep_line in grep_output:
                exists = re.search('(\d+):DEFINE_(\w*)\((\w*), (.*), (.*)\);', grep_line)

                if exists == None:
                        continue
                else:
                        if exists.group(3) == param_name.lower():
                                yaml_test_param[dsp_name][test_name][param_name] = exists.group(5)
                        else:
                                continue


# parse dsp_<dsp>.tests.yaml file and store it in main_dict

def parse_file(filename, platform, board_name):
	global main_dict

        filepath = dsp_yaml_path + '/' + filename
        y = yaml.safe_load(open(filepath, 'r'))
        DSP_name = y['DSP']['NAME']

        for key in y:
                if key == "DSP":
                        continue
                else:
                        if y[key]["PLATFORM"][platform] == None:
                                continue
                        else:
                                test_name = key.split('#')[1]
                                help_info = y[key]["HELP_INFO"]
                                param_info = y[key]["PARAM"] # type(param_info) == dict()

                                #verify that the board uses said test
                                if (board_name in y[key]["PLATFORM"][platform]) or (y[key]["PLATFORM"][platform] == "ALL"):
                                        main_dict[DSP_name][test_name] = dict([('HELP_INFO', help_info), ("PARAM", {})]) # adding help info
                                        # now we parse through the parameters to find the right ones to add to add to main_dict[DSP_name][test_name]['PARAM']
                                        for p in param_info:
                                                # parameters have the format <parameter>@<platform>#ALL or <parameter>@<board_name>
                                                # if both <platform>#ALL and <parameter>@<board_name> are both present for said board, <parameter>@<board_name> will take priority
                                                p_items = p.split('@')
                                                check_all = platform + "#ALL"

                                                if check_all in p_items:
                                                        # check to see if main_dict[DSP_name][test_name]["PARAM"] has been created yet
                                                        main_dict[DSP_name][test_name]["PARAM"][p_items[0]] = y[key]["PARAM"][p]
                                                elif board_name in p:
                                                        main_dict[DSP_name][test_name]["PARAM"][p_items[0]] = y[key]["PARAM"][p]
                                                elif p_items[1] == "ALL":
                                                        main_dict[DSP_name][test_name]["PARAM"][p_items[0]] = y[key]["PARAM"][p]


# self-explanatory name; goes through main_dict and creates yaml_test_param by calling all the helper functions above

def create_yaml_dict(main_dict):
	for dsp in main_dict.keys():
		dsp_path = _get_dsp_path(dsp)
		
		if dsp == "TOMAHAWK" or dsp == "TRIDENT":
			for test_name in main_dict[dsp]:
				_search_func_file(dsp, '../../../../../../sdk-xgs-robo-6.4.8/src/customer', test_name, "trident_diagsp.cpp")
		elif dsp == "GE":
			for test_name in main_dict[dsp]:
				_search_func_file(dsp, '../../../dsp/bcm_ge_phy', test_name, "bcm_ge_phy_diagsp.cpp")

        	elif dsp == 'MVL10P' or dsp == 'MVL4P':
                	for test_name in main_dict[dsp]:
                        	for param_name in main_dict[dsp][test_name]['PARAM'].keys():
                                	if param_name == "unstable_network":
                                        	#cpp_path = '../../../common/cmnlib_diagsp/diagsp_common.cpp'
                                        	#_search_func_file_mvlp(dsp, test_name, 'unstable_network', cpp_path)
						yaml_test_param[dsp][test_name][param_name] = "if true, teardown/reconnect from/to redis before/after test_hdl"
                                	else:
                                        	dsp_path = '../../../dsp/mvl4port'
                                        	func_test = search_test_function(dsp_path, test_name)
                                        	cpp_name = get_func_cpp(func_test, dsp_path)
                                        	cpp_path = dsp_path + '/' + cpp_name
                                        	_search_func_file_mvlp(dsp, test_name, param_name, cpp_path)
		else:
			for test_name in main_dict[dsp]:


				# grab the name of the function for given test
				func_test = search_test_function(dsp_path, test_name)

				# parse through the parameters needed for that test
				cpp_name = get_func_cpp(func_test, dsp_path)
				_search_func_file(dsp, dsp_path, test_name, cpp_name)


# filename = <BOARD_NAME>_dsp.xml

def write_xml_file(main_dict, yaml_test_param):
	sorted_list = sorted(main_dict)

	print("Writing XML file ...\n")

	filename = board_name + "_dsp.xml"
	f = open(filename, 'ab')
	f.write("<board>\n")

	count = 0

	for dsp in sorted_list:
		f.write("\t<DSP>\n")

		if count == 0:
			f.write("\t\t<DSP_name>" + dsp + "</DSP_name>\n")
			count += 1
		else:
			continue

		for test_name in sorted(main_dict[dsp]):
			f.write("\t\t<test>\n\t\t\t<test_name>" + test_name + "</test_name>\n")
			for help_or_param, str_or_dict in main_dict[dsp][test_name].items():
				if help_or_param == "HELP_INFO":
					if str_or_dict == None:
						f.write("\t\t\t<help>\"\"</help>\n")
					else:
						str_or_dict = str_or_dict.replace('&', '&amp;')
						f.write("\t\t\t<help>" + str_or_dict + "</help>\n")

				elif help_or_param == "PARAM":
					if main_dict[dsp][test_name]["PARAM"]:
						for p in sorted(main_dict[dsp][test_name]["PARAM"].keys()):
							if p == "run_cnt":
								f.write("\t\t\t<param>\n")
								f.write("\t\t\t\t<param_name>" + str(p) + "</param_name>\n")
								f.write("\t\t\t\t<param_value>" + str(main_dict[dsp][test_name]["PARAM"][p]) + "</param_value>\n")
								f.write("\t\t\t\t<param_info>Number of iterations to run</param_info>\n")
								f.write("\t\t\t</param>\n")
							elif p == "timeout":
								f.write("\t\t\t<param>\n")
								f.write("\t\t\t\t<param_name>" + str(p) + "</param_name>\n")
								f.write("\t\t\t\t<param_value>" + str(main_dict[dsp][test_name]["PARAM"][p]) + "</param_value>\n")
								f.write("\t\t\t\t<param_info>Maximum duration allowed (seconds)</param_info>\n")
								f.write("\t\t\t</param>\n")
							elif p not in yaml_test_param[dsp][test_name].keys():
								f.write("\t\t\t<param>\n")
								f.write("\t\t\t\t<param_name>" + str(p) + "</param_name>\n")
								f.write("\t\t\t\t<param_value>" + str(main_dict[dsp][test_name]["PARAM"][p]) + "</param_value>\n")
								f.write("\t\t\t\t<param_info>\" \"</param_info>\n")
								f.write("\t\t\t</param>\n")
							else:
								f.write("\t\t\t<param>\n")
								f.write("\t\t\t\t<param_name>" + str(p) + "</param_name>\n")
								f.write("\t\t\t\t<param_value>" + str(main_dict[dsp][test_name]["PARAM"][p]) + "</param_value>\n")
								f.write("\t\t\t\t<param_info>" + yaml_test_param[dsp][test_name][p] + "</param_info>\n")
								f.write("\t\t\t</param>\n")
			f.write("\t\t</test>\n")
		f.write("\t</DSP>\n")
		count = 0
	f.write("</board>")
	f.close()


# used for testing. prints out dictionaries nicely

def pretty(d, indent=0):
   for key, value in d.iteritems():
      print '\t' * indent + str(key)
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print '\t' * (indent+1) + str(value)



if __name__ == '__main__':
	print(board_name)
	if valid_board(board_name, get_yaml_table()) == "ERROR":
		print(board_name + " is an invalid board name")


	else:
		for file_name in os.listdir(dsp_yaml_path):
			if valid_file(file_name):
				parse_file(file_name, valid_board(board_name, get_yaml_table()), board_name)
			else:
				continue


		create_yaml_dict(main_dict)
	


		name_of_file = board_name + "_dsp.xml"
		try:
			os.remove(name_of_file)
		except OSError:
			pass

		write_xml_file(main_dict, yaml_test_param)



