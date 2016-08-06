import sys
import os.path
import zipfile
import urllib.request

print("\nCodeSmithy bootstrap build")
print("--------------------------\n")

print("Step 1a: Fetching CodeSmithy code from https://github.com/CodeSmithyIDE/CodeSmithy/archive/master.zip")
urllib.request.urlretrieve('https://github.com/CodeSmithyIDE/CodeSmithy/archive/master.zip', 'master.zip')

print("Step 1b: Unzipping master.zip\n")
zip_ref = zipfile.ZipFile('master.zip', 'r')
zip_ref.extractall('.')
zip_ref.close()

print("Step 2: Finding compilers")
compilers = []
foundMSVC14 = os.path.isfile('C:/Program Files (x86)/Microsoft Visual Studio 14.0/Common7/IDE/devenv.exe')
if foundMSVC14:
    compilers.append("Visual Studio 2015")

print("The following compilers have been found")
for i, c in enumerate(compilers):
    print(str(i+1) + ") " + c)

if len(compilers) == 0:
    print("No suitable compilers found, exiting")
    sys.exit();

selectedCompiler = (int(input("Select the compiler to use: ")) - 1)
