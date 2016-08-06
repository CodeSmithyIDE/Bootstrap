import sys
import os.path
import subprocess
import zipfile
import urllib.request

print("\nCodeSmithy bootstrap build")
print("--------------------------\n")

print("Step 1a: Fetching libgit2 code from https://github.com/CodeSmithyIDE/libgit2/archive/master.zip")
urllib.request.urlretrieve("https://github.com/CodeSmithyIDE/libgit2/archive/master.zip", "libgit2-master.zip")

print("Step 1b: Unzipping libgit2-master.zip\n")
zip_ref = zipfile.ZipFile("libgit2-master.zip", "r")
zip_ref.extractall(".")
zip_ref.close()

print("Step 1c: Fetching CodeSmithy code from https://github.com/CodeSmithyIDE/CodeSmithy/archive/master.zip")
urllib.request.urlretrieve("https://github.com/CodeSmithyIDE/CodeSmithy/archive/master.zip", "CodeSmithy-master.zip")

print("Step 1d: Unzipping CodeSmithy-master.zip\n")
zip_ref = zipfile.ZipFile("CodeSmithy-master.zip", "r")
zip_ref.extractall(".")
zip_ref.close()

print("Step 2: Finding compilers")
compilers = []
compilerPaths = []
foundMSVC14 = os.path.isfile("C:/Program Files (x86)/Microsoft Visual Studio 14.0/Common7/IDE/devenv.exe")
if foundMSVC14:
    compilers.append("Visual Studio 2015")
    compilerPaths.append("C:/Program Files (x86)/Microsoft Visual Studio 14.0/Common7/IDE/devenv.exe")

print("The following compilers have been found")
for i, c in enumerate(compilers):
    print(str(i+1) + ") " + c)

if len(compilers) == 0:
    print("No suitable compilers found, exiting")
    sys.exit();

selectedCompiler = (int(input("Select the compiler to use: ")) - 1)
print("")

print("Step 3: Building CodeSmithyMake")
codeSmithyMakeMakefilePath = ""
if compilers[selectedCompiler] == "Visual Studio 2015":
    codeSmithyMakeMakefilePath = "CodeSmithy-master/Make/Makefiles/VC14/CodeSmithyMake.sln"
rc = subprocess.call([compilerPaths[selectedCompiler], codeSmithyMakeMakefilePath, "/build", "Debug"])
if rc == 0:
    print("CodeSmithyMake built successfully")
