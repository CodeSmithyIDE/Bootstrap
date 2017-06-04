import platform
import sys
import os.path
import subprocess
import zipfile
import urllib.request
import shutil
from pathlib import Path

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

shutil.rmtree("Downloads", ignore_errors=True)
shutil.rmtree("Build", ignore_errors=True)

Path("Downloads").mkdir(exist_ok=True)
Path("Build").mkdir(exist_ok=True)

def downloadAndUnzip(substep, organization, name, url):
    print("Step 1" + substep + ": Fetching " + name + " code from " + url, flush=True)
    downloadPath = "Downloads/" + name + "-master.zip"
    extractPathPrefix = "Build"
    if len(organization) > 0:
        Path("Downloads/" + organization).mkdir(exist_ok=True)
        Path("Build/" + organization).mkdir(exist_ok=True)
        downloadPath = "Downloads/" + organization + "/" + name + "-master.zip"
        extractPathPrefix = "Build/" + organization 
    urllib.request.urlretrieve(url, downloadPath)
    print("Step 1" + substep + ": Unzipping " + downloadPath + "\n", flush=True)
    zip_ref = zipfile.ZipFile(downloadPath, "r")
    zip_ref.extractall(extractPathPrefix)
    zip_ref.close()
    shutil.rmtree(extractPathPrefix + "/" + name, ignore_errors=True)
    os.rename(extractPathPrefix + "/" + name + "-master", extractPathPrefix + "/" + name)
    return

downloadAndUnzip("a", "Ishiko", "Errors", "https://github.com/CodeSmithyIDE/Errors/archive/master.zip")
downloadAndUnzip("b", "Ishiko", "Process", "https://github.com/CodeSmithyIDE/Process/archive/master.zip")
downloadAndUnzip("c", "Ishiko", "WindowsRegistry", "https://github.com/CodeSmithyIDE/WindowsRegistry/archive/master.zip")
downloadAndUnzip("d", "Ishiko", "FileTypes", "https://github.com/CodeSmithyIDE/FileTypes/archive/master.zip")
downloadAndUnzip("e", "Ishiko", "TestFramework", "https://github.com/CodeSmithyIDE/TestFramework/archive/master.zip")
downloadAndUnzip("f", "", "libgit2", "https://github.com/CodeSmithyIDE/libgit2/archive/master.zip")
downloadAndUnzip("g", "", "wxWidgets", "https://github.com/CodeSmithyIDE/wxWidgets/archive/master.zip")
downloadAndUnzip("h", "CodeSmithyIDE", "CodeSmithy", "https://github.com/CodeSmithyIDE/CodeSmithy/archive/master.zip")

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
    sys.exit(-1);

selectedCompiler = (int(input("Select the compiler to use: ")) - 1)
print("")

# CMake is not easily buildable on Windows so we rely on a binary distribution
print("Step 3: Installing CMake\n", flush=True)
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

print("Step 4: Building libgit2", flush=True)
os.chdir("Build/libgit2")
rc = subprocess.call(["../../" + cmakePath, "."])
rc = subprocess.call(["../../" + cmakePath, "--build", "."])
if rc == 0:
    print("libgit2 build successfully")
else:
    print("Failed to build libgit2, exiting")
    sys.exit(-1)
os.chdir("../..")
print("")

os.environ["ISHIKO"] = os.getcwd() + "/Build/Ishiko"
os.environ["CODESMITHY"] = os.getcwd() + "/Build/CodeSmithyIDE/CodeSmithy"

print("Step 5: Building Process", flush=True)
processMakefilePath = ""
if compilers[selectedCompiler] == "Visual Studio 2015":
    processMakefilePath = "Build/Ishiko/Process/Makefiles/VC14/IshikoProcess.sln"
rc = subprocess.call([compilerPaths[selectedCompiler], processMakefilePath, "/build", "Debug"])
if rc == 0:
    print("Process built successfully")
else:
    print("Failed to build Process, exiting")
    sys.exit(-1)
print("")

print("Step 6: Building CodeSmithyCore", flush=True)
codeSmithyCoreMakefilePath = ""
if compilers[selectedCompiler] == "Visual Studio 2015":
    codeSmithyCoreMakefilePath = "Build/CodeSmithyIDE/CodeSmithy/Core/Makefiles/VC14/CodeSmithyCore.sln"
rc = subprocess.call([compilerPaths[selectedCompiler], codeSmithyCoreMakefilePath, "/build", "Debug"])
if rc == 0:
    print("CodeSmithyCore built successfully")
else:
    print("Failed to build CodeSmithyCore, exiting")
    sys.exit(-1)
print("")

print("Step 7: Building CodeSmithyMake", flush=True)
codeSmithyMakeMakefilePath = ""
codeSmithyMakePath = ""
if compilers[selectedCompiler] == "Visual Studio 2015":
    codeSmithyMakeMakefilePath = "Build/CodeSmithyIDE/CodeSmithy/Make/Makefiles/VC14/CodeSmithyMake.sln"
    codeSmithyMakePath = "Build/CodeSmithyIDE/CodeSmithy/Bin/Win32/CodeSmithyMake.exe"
rc = subprocess.call([compilerPaths[selectedCompiler], codeSmithyMakeMakefilePath, "/build", "Debug"])
if rc == 0:
    print("CodeSmithyMake built successfully")
else:
    print("Failed to build CodeSmithyMake, exiting")
    sys.exit(-1)
print("")

def buildWithCodeSmithyMake(name, makefile):
    rc = subprocess.call([codeSmithyMakePath, makefile])
    if rc == 0:
        print(name + " built successfully")
    else:
        print("Failed to build " + name + ", exiting")
        sys.exit(-1)
    return

print("Step 8: Building Errors", flush=True)
buildWithCodeSmithyMake("Errors", "Build/Ishiko/Errors/Makefiles/VC14/IshikoErrors.sln")
print("")

print("Step 9: Building TestFrameworkCore", flush=True)
buildWithCodeSmithyMake("TestFrameworkCore", "Build/Ishiko/TestFramework/Core/Makefiles/VC14/IshikoTestFrameworkCore.sln")
print("")

print("Step 10: Building WindowsRegistry", flush=True)
buildWithCodeSmithyMake("WindowsRegistry", "Build/Ishiko/WindowsRegistry/Makefiles/VC14/IshikoWindowsRegistry.sln")
print("")

print("Step 11: Building FileTypes", flush=True)
buildWithCodeSmithyMake("FileTypes", "Build/Ishiko/FileTypes/Makefiles/VC14/IshikoFileTypes.sln")
print("")

print("Step 12: Building CodeSmithyUICore", flush=True)
buildWithCodeSmithyMake("CodeSmithyUICore", "Build/CodeSmithyIDE/CodeSmithy/UICore/Makefiles/VC14/CodeSmithyUICore.sln")
print("")

print("Step 13: Building CodeSmithyUIElements", flush=True)
buildWithCodeSmithyMake("CodeSmithyUIElements", "Build/CodeSmithyIDE/CodeSmithy/UIElements/Makefiles/VC14/CodeSmithyUIElements.sln")
print("")

print("Step 14: Building CodeSmithyUIImplementation", flush=True)
buildWithCodeSmithyMake("CodeSmithyUIImplementation", "Build/CodeSmithyIDE/CodeSmithy/UIImplementation/Makefiles/VC14/CodeSmithyUIImplementation.sln")
print("")

print("Step 15: Building CodeSmithy", flush=True)
buildWithCodeSmithyMake("CodeSmithy", "Build/CodeSmithyIDE/CodeSmithy/UI/Makefiles/VC14/CodeSmithy.sln")
print("")

print("Step 16: Building CodeSmithyCore tests", flush=True)
buildWithCodeSmithyMake("CodeSmithyCore", "Build/CodeSmithyIDE/CodeSmithy/Tests/Core/Makefiles/VC14/CodeSmithyCoreTests.sln")
print("")

print("Step 17: Building CodeSmithyMake tests", flush=True)
buildWithCodeSmithyMake("CodeSmithyMake", "Build/CodeSmithyIDE/CodeSmithy/Tests/Make/Makefiles/VC14/CodeSmithyMakeTests.sln")
print("")
