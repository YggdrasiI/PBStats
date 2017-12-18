To inform Pylint or other static code analyzer about the Civ4 SDK
function you could use this package. The folder PythonApi contains
a set of classes/function stubs.

Setup:
0. It exists several ways to install Pylint. One variant will be described here.
   Skip this step if Pylint is already installed.
   • wget "https://bootstrap.pypa.io/get-pip.py"
   • python get-pip.py 
   • python -m pip install pylint

1. Add the following lines to your Pylint configuration.

      init-hook="API='[absolute path of this folder]\Civ4PythonApi';
      CIV4='C:\YourPath\Civ4'; MOD='YourOptionalModName';
      import sys; sys.path.append(API); import Civ4Paths;
      sys.path.extend(Civ4Paths.civ4_paths(CIV4, MOD))"

  Notes:
    - Join above lines into one! Pylint does not allow to split arguments on multiple lines.
    - Adapt the folders and mod name to your requirements. Use Slashes on Non-Windows OS.
    - Use '--init-hook' but not 'init-hook' if you use it as arguments.
      The arguments after = should always be enquoted with double quotes,
      but not single quotes.


2. Unfortunately, the code of Civ4 does violate many PEP8 styling rules. We suggest
   to disable several warnings to made the critical warings/errors more present.
   Add following to your Pylint setup:

    disable=too-many-lines,no-init,old-style-class,no-self-use,unused-argument,too-few-public-methods,too-many-public-methods,interface-not-implemented,too-many-arguments,too-many-instance-attributes,too-many-branches,missing-docstring,unused-import,invalid-name,wildcard-import,unused-wildcard-import,superfluous-parens,too-many-return-statements,too-many-locals,too-many-statementas,line-too-long


3. As example we also include a batch script (pylint.bat)
