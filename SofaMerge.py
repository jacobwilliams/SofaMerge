#!/usr/bin/env python
"""
Combine all the SOFA source files into one module

Example Usage: ./SofaMerge.py '~/sofa/20131202_d/f77/src/' > sofa.f

Tested with the 2013-12-02 release of SOFA.
http://www.iausofa.org/current_F.html

"""
__appname__ = 'SofaMerge.py'
__version__ = '0.0.2'
__author__  = 'Jacob Williams'

##########################################
def rreplace(s, old, new, occurrence):
	'''replace last occurrence of old with new'''
	li = s.rsplit(old, occurrence)
	return new.join(li)
	
##########################################
#  Some text in the files:
##########################################

_sofa_boilerplate="""
*+----------------------------------------------------------------------
*
*  Copyright (C) 2013
*  Standards Of Fundamental Astronomy Board
*  of the International Astronomical Union.
*
*  =====================
*  SOFA Software License
*  =====================
*
*  NOTICE TO USER:
*
*  BY USING THIS SOFTWARE YOU ACCEPT THE FOLLOWING SIX TERMS AND
*  CONDITIONS WHICH APPLY TO ITS USE.
*
*  1. The Software is owned by the IAU SOFA Board ("SOFA").
*
*  2. Permission is granted to anyone to use the SOFA software for any
*     purpose, including commercial applications, free of charge and
*     without payment of royalties, subject to the conditions and
*     restrictions listed below.
*
*  3. You (the user) may copy and distribute SOFA source code to others,
*     and use and adapt its code and algorithms in your own software,
*     on a world-wide, royalty-free basis.  That portion of your
*     distribution that does not consist of intact and unchanged copies
*     of SOFA source code files is a "derived work" that must comply
*     with the following requirements:
*
*     a) Your work shall be marked or carry a statement that it
*        (i) uses routines and computations derived by you from
*        software provided by SOFA under license to you; and
*        (ii) does not itself constitute software provided by and/or
*        endorsed by SOFA.
*
*     b) The source code of your derived work must contain descriptions
*        of how the derived work is based upon, contains and/or differs
*        from the original SOFA software.
*
*     c) The names of all routines in your derived work shall not
*        include the prefix "iau" or "sofa" or trivial modifications
*        thereof such as changes of case.
*
*     d) The origin of the SOFA components of your derived work must
*        not be misrepresented;  you must not claim that you wrote the
*        original software, nor file a patent application for SOFA
*        software or algorithms embedded in the SOFA software.
*
*     e) These requirements must be reproduced intact in any source
*        distribution and shall apply to anyone to whom you have
*        granted a further right to modify the source code of your
*        derived work.
*
*     Note that, as originally distributed, the SOFA software is
*     intended to be a definitive implementation of the IAU standards,
*     and consequently third-party modifications are discouraged.  All
*     variations, no matter how minor, must be explicitly marked as
*     such, as explained above.
*
*  4. You shall not cause the SOFA software to be brought into
*     disrepute, either by misuse, or use for inappropriate tasks, or
*     by inappropriate modification.
*
*  5. The SOFA software is provided "as is" and SOFA makes no warranty
*     as to its use or performance.   SOFA does not and cannot warrant
*     the performance or results which the user may obtain by using the
*     SOFA software.  SOFA makes no warranties, express or implied, as
*     to non-infringement of third party rights, merchantability, or
*     fitness for any particular purpose.  In no event will SOFA be
*     liable to the user for any consequential, incidental, or special
*     damages, including any lost profits or lost savings, even if a
*     SOFA representative has been advised of such damages, or for any
*     claim by any third party.
*
*  6. The provision of any version of the SOFA software under the terms
*     and conditions specified herein does not imply that future
*     versions will also be made available under the same terms and
*     conditions.
*
*  In any published work or commercial product which uses the SOFA
*  software directly, acknowledgement (see www.iausofa.org) is
*  appreciated.
*
*  Correspondence concerning SOFA software should be addressed as
*  follows:
*
*      By email:  sofa@ukho.gov.uk
*      By post:   IAU SOFA Center
*                 HM Nautical Almanac Office
*                 UK Hydrographic Office
*                 Admiralty Way, Taunton
*                 Somerset, TA1 2DN
*                 United Kingdom
*
*-----------------------------------------------------------------------
"""

_sofa_finished = """*  Finished.

"""

_sofa_divider = """* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

"""

##########################################
def cleansofa(srcdir):
	'''main routine : process all the files.'''

	import glob
	import time
	import sys
	import re
	
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

				#remove some unwanted text:
				data = data.replace(_sofa_boilerplate,'')
				data = data.replace(_sofa_finished,'')
				data = data.replace(_sofa_divider,'')
								
				#Remove all the function declarations in the routines:
				# example: DOUBLE PRECISION iau_ANP	
				data = data.replace('      DOUBLE PRECISION iau_', c+'     DOUBLE PRECISION iau_')
				data = data.replace('     :                 iau_', c+'    :                 iau_')
								
				#append this routine:
				module_content = module_content + c+div + '\n' + data + c+div + '\n'+ '\n'
		
		else:
			print('Error parsing file: ' + f)
			sys.exit(0)
	
	##########
	# Fix the lines like this: '+2004.191898     D0, &'
	re1='(\\d)'	# Any Single Digit
	re2='(\\s+)'	# White Space
	re3='(D)'	# Exponent Character
	rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
	for line in module_content.split('\n'):
		if (line[0:]!='     :'):  #don't print blank continuation lines
			m = rg.search(line)
			if m:
				#remove the whitespace between the number and the 'D'
				line = line[0:m.span()[0]]+m.group(1)+m.group(3)+line[m.span()[1]:]
			print(line)
	##########
			
	# Could also include some fixed-to-free conversions here
		
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
