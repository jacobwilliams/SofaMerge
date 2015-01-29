# SofaMerge
A simple script to make one module from all the SOFA files.

Description
--------------------

This is a little Python script to make your life easier if you are using the Fortran 77 version of the [Standards of Fundamental Astronomy (SOFA) library](http://www.iausofa.org/current_F.html).  All it does is take the individual files and merge them into one Fortran module file.  It currently makes no attempt to convert the files to free format (although this could easily be added).

Usage
--------------------

The script takes a single argument, which is the location of the SOFA source directory.  For example:

```./SofaMerge.py '~/sofa/20131202_d/f77/src/' > sofa.f```

