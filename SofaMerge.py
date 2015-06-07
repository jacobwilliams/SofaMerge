#!/usr/bin/env python
"""
Combine all the SOFA source files into one module

Example Usage: 

	# merge all the SOFA files:
	python SofaMerge.py ./sofa/20150209_a/f77/src/ > sofa.f
	
	#
	# for fixed-to-free conversion, could use: 
	#   https://github.com/ylikx/fortran-legacy-tools
	#
	python fixed2free2.py sofa.f > sofa.f90
	python flowercase.py sofa.f90 > sofa_module.f90

Tested with the 2013 and 2015 releases of SOFA.
http://www.iausofa.org/current_F.html

"""
__appname__ = 'SofaMerge.py'
__version__ = '0.0.4'
__author__  = 'Jacob Williams'

import glob
import time
import sys
import re

##########################################
def rreplace(s, old, new, occurrence):
	'''replace last occurrence of old with new'''
	li = s.rsplit(old, occurrence)
	return new.join(li)
	
##########################################
#  Some text in the files:
##########################################

#the SOFA boilerplate text:
_sofa_boilerplate_start = '\n\\*\\+----------------------------------------------------------------------'
_sofa_boilerplate_end = '\\*-----------------------------------------------------------------------\n'
_sofa_boilerplate_re = '('+_sofa_boilerplate_start+')(.*?)('+_sofa_boilerplate_end+')'
_sofa_boilerplate_rg = re.compile(_sofa_boilerplate_re,re.IGNORECASE|re.DOTALL)

_sofa_finished = """*  Finished.

"""

_sofa_divider = """* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

"""

##########################################
def cleansofa(srcdir):
	'''main routine : process all the files.'''
	
	module_name = "sofa_module"	
	div = "***********************************************************************"
	
	c = '*'  #comment character
	
	#file header:
	print(c+div)
	print("      module "+module_name)
	print(c+div)
	print(c)
	print(c+" this file was automatically generated using the create_sofa_module.py script")
	print(c+" Generated on: " + time.strftime("%c"))
	print(c)
	print(c+div)
	print(" ")
	print("      implicit none")
	print("      public")
	print("      contains")
	print(" ")
	print(c+div)
	print(" ")

	#get list of files in the directory:
	html_file_list = sorted(glob.glob(srcdir+"*.for"))

	module_content = ''
	get_boilerplate = True
	
	#loop through each file:
	for f in html_file_list:
	
		#open this file and read it:
		data = open(f).read()
		
		#is it a subroutine or a function?
		isub  = data.find('SUBROUTINE')
		ifunc = data.find('FUNCTION')	
		
		is_sub  = isub>0  and (ifunc<0 or (ifunc>0 and isub<ifunc))
		is_func = ifunc>0 and (isub<0  or (isub>0 and ifunc<isub))
		
		#get function or subroutine name
		j = data.find('(')        #this should be after the procedure name
		
		if ( j>-1 and (is_sub or is_func) ):
		
			if (is_sub):
				i = isub + 10
			else:
				i = ifunc + 8
		
			bit = data[i:j]	
			name = bit.strip()	
			if (name):
			
				#to the final END statement, have to add SUBROUTINE or FUNCTION
				if (is_sub):		#it's a subroutine
					data = rreplace(data, 'END', 'END SUBROUTINE '+name, 1)
				elif (is_func):		#it's a function
					data = rreplace(data, 'END', 'END FUNCTION '+name, 1)
				else:				
					print('Error parsing file: '+name)
					sys.exit(0)

				#save the boilerplate, so it can be added to the end of the file:
				# [only need to do this once]
				if (get_boilerplate):
					m = _sofa_boilerplate_rg.search(data)
					if m:
						c1=m.group(1)
						c2=m.group(2)
						c3=m.group(3)
						_sofa_boilerplate = c1+c2+c3
						get_boilerplate = False
				
				#remove some unwanted text:
				data = re.sub(_sofa_boilerplate_re,'',data, flags=re.DOTALL)
				data = data.replace(_sofa_finished,'')
				data = data.replace(_sofa_divider,'')
								
				#Remove all the function declarations in the routines:
				# example: DOUBLE PRECISION iau_ANP	
				data = data.replace('      DOUBLE PRECISION iau_', c+'     DOUBLE PRECISION iau_')
				data = data.replace('     :                 iau_', c+'    :                 iau_')
				
				#Also update relational operators:
				data = data.replace('.GT.','>')
				data = data.replace('.LT.','<')
				data = data.replace('.EQ.','==')
				data = data.replace('.GE.','>=')
				data = data.replace('.LE.','<=')
				data = data.replace('.NE.','/=')
				
				#append this routine:
				module_content = module_content + c+div + '\n' + data + c+div + '\n'+ '\n'
		
		else:
			print('Error parsing file: ' + f)
			sys.exit(0)
	
	##########
		
	# Fix the lines like this: '+2004.191898     D0, &'
	re1='(\\d)'		# Any Single Digit
	re2='(\\s+)'	# White Space
	re3='(D)'		# Exponent Character
	rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
	for line in module_content.split('\n'):
		if (line[0:]!='     :'):  #don't print blank continuation lines
			
			#skip comment lines:
			check = True
			if (len(line)>0): check = (line[0]!='*')
			
			if (check):
				m = rg.search(line)
				if m:
					#remove the whitespace between the number and the 'D'
					line = line[0:m.span()[0]]+m.group(1)+m.group(3)+line[m.span()[1]:]
			
			print(line)

	##########
	
	#finished with all the files:
	print(c+div)
	print("      end module "+module_name)
	print(c+div)
	print(" ")
	print(_sofa_boilerplate)

###########################################
if __name__ == '__main__':
	'''Main program'''
	
	import argparse	
	
	parser = argparse.ArgumentParser(description='SofaMerge : it merges all the SOFA files into one module.')
	parser.add_argument('srcdir',help='Directory containing the SOFA source files.')
	args = parser.parse_args()
	
	cleansofa(args.srcdir)
