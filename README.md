# SofaMerge
A simple script to make one module from all the SOFA files.

Description
--------------------

This is a little Python script to make your life easier if you are using the Fortran 77 version of the [Standards of Fundamental Astronomy (SOFA) library](https://www.iausofa.org/current-software).  All it does is take the individual files and merge them into one Fortran module file.  It currently makes no attempt to convert the files to free format (although this could easily be added).

Usage
--------------------

The script takes a single argument, which is the location of the SOFA source directory.  For example:

```python SofaMerge.py ~/sofa/20150209_a/f77/src/ > sofa.f```

To also convert the file to free-form source, you could then use [fortran-legacy-tools](https://github.com/ylikx/fortran-legacy-tools) like so:

```python fixed2free2.py sofa.f > sofa.f90```

```python flowercase.py sofa.f90 > sofa_module.f90```
