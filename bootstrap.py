import sys
import platform
import os.path
import subprocess
import zipfile
import urllib.request

print("\nCodeSmithy bootstrap build")
print("--------------------------\n")

platformName = platform.system()
is64bit = False
if platform.machine() == "AMD64":
    is64bit = True
    
print("Platform: " + platformName)
if is64bit:
    print("Architecture: 64 bit")
else:
    print("Architecture: 32 bit")
print("")

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

# CMake is not easily buildable on Windows so we rely on a binary distribution
print("Step 3: Installing CMake\n")
cmakePath = ""
if platformName == "Windows":
    if is64bit:
        zip_ref = zipfile.ZipFile("CMake/cmake-3.6.1-win64-x64.zip", "r")
        cmakePath = "cmake-3.6.1-win64-x64/bin/cmake.exe"
    else:
        zip_ref = zipfile.ZipFile("CMake/cmake-3.6.1-win32-x86.zip", "r")
        cmakePath = "cmake-3.6.1-win32-x86/bin/cmake.exe"
    zip_ref.extractall(".")
    zip_ref.close()

print("Step 4: Building libgit2")
rc = subprocess.call([cmakePath, "--build", "libgit2-master"])
if rc == 0:
    print("libgit2 build successfully")

print("Step 5: Building CodeSmithyMake")
codeSmithyMakeMakefilePath = ""
if compilers[selectedCompiler] == "Visual Studio 2015":
    codeSmithyMakeMakefilePath = "CodeSmithy-master/Make/Makefiles/VC14/CodeSmithyMake.sln"
rc = subprocess.call([compilerPaths[selectedCompiler], codeSmithyMakeMakefilePath, "/build", "Debug"])
if rc == 0:
    print("CodeSmithyMake built successfully")
