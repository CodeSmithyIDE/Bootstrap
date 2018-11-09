import platform
import os
import sys
import subprocess
import shutil
from pathlib import Path
from output import Output
from argparser import ArgParser
from state import State
from projects import Projects
from download import Downloader
from cmake import CMake
from compilers import Compilers

print("\nCodeSmithy bootstrap build")
print("--------------------------\n")

output = Output()
args = ArgParser().parse()
state = State()

if state.previous_state_found:
    resume = ""
    while resume != "y" and resume != "n":
        resume = input(
            "Previous execution detected. Do you want to resume it? [y/n] ")
    if resume == "n":
        state.reset()
        shutil.rmtree("Build", ignore_errors=True)

platform_name = platform.system()
is64bit = False
if platform.machine() == "AMD64":
    is64bit = True

print("Platform: " + platform_name)
if is64bit:
    print("Architecture: 64 bit")
else:
    print("Architecture: 32 bit")
print("")

Path("Build").mkdir(exist_ok=True)

downloader = Downloader()
compilers = Compilers()
cmake = CMake()

output.print_step_title("Downloading source packages")
if state.download_complete == False:
    shutil.rmtree("Downloads", ignore_errors=True)
    downloader.download()
else:
    print("    Using previous execution")
state.set_download_complete()
output.next_step()

print("")
output.print_step_title("Finding compilers")
if state.selected_compiler == "":
    compilers.show_compiler_list()
    if len(compilers.compilers) == 0:
        print("")
        print("ERROR: No compilers found, exiting")
        sys.exit(-1);
    selected_compiler_index = (int(input("    Select the compiler to use: ")) - 1)
    compiler = compilers.compilers[selected_compiler_index]
else:
    compiler = compilers.find_by_name(state.selected_compiler)
    print("    Using previous selection: " + compiler.name)
state.set_selected_compiler(compiler.name)
output.next_step()

# CMake is not easily buildable on Windows so we rely on a binary distribution
print("")
output.print_step_title("Installing CMake")
if state.cmake_path == "":
    cmake.install(platform_name, is64bit)
    print("    CMake installed successfully")
else:
    cmake.path = state.cmake_path
    print("    Using previous installation: " + cmake.path)
state.set_cmake_path(cmake.path)
output.next_step()

os.environ["ISHIKO"] = os.getcwd() + "/Build/Ishiko"
os.environ["CODESMITHY"] = os.getcwd() + "/Build/CodeSmithyIDE/CodeSmithy"

print("")
output.print_step_title("Unzipping source packages")
downloader.unzip()
output.next_step()

print("")
output.print_step_title("Building libgit2")
cmake.compile()
output.next_step()

projects = Projects()
projects.build(compiler, output)

codeSmithyMakePath = "Build/CodeSmithyIDE/CodeSmithy/Bin/Win32/CodeSmithyMake.exe"

def buildWithCodeSmithyMake(name, makefile):
    rc = subprocess.call([codeSmithyMakePath, makefile])
    if rc == 0:
        print(name + " built successfully")
    else:
        print("Failed to build " + name + ", exiting")
        sys.exit(-1)
    return

print("Step 9: Building Errors", flush=True)
buildWithCodeSmithyMake("Errors", "Build/Ishiko/Errors/Makefiles/VC14/IshikoErrors.sln")
print("")

print("Step 10: Building TestFrameworkCore", flush=True)
buildWithCodeSmithyMake("TestFrameworkCore", "Build/Ishiko/TestFramework/Core/Makefiles/VC14/IshikoTestFrameworkCore.sln")
print("")

print("Step 11: Building WindowsRegistry", flush=True)
buildWithCodeSmithyMake("WindowsRegistry", "Build/Ishiko/WindowsRegistry/Makefiles/VC14/IshikoWindowsRegistry.sln")
print("")

print("Step 12: Building FileTypes", flush=True)
buildWithCodeSmithyMake("FileTypes", "Build/Ishiko/FileTypes/Makefiles/VC14/IshikoFileTypes.sln")
print("")

print("Step 13: Building CodeSmithyUICore", flush=True)
buildWithCodeSmithyMake("CodeSmithyUICore", "Build/CodeSmithyIDE/CodeSmithy/UICore/Makefiles/VC14/CodeSmithyUICore.sln")
print("")

print("Step 14: Building CodeSmithyUIElements", flush=True)
buildWithCodeSmithyMake("CodeSmithyUIElements", "Build/CodeSmithyIDE/CodeSmithy/UIElements/Makefiles/VC14/CodeSmithyUIElements.sln")
print("")

print("Step 15: Building CodeSmithyUIImplementation", flush=True)
buildWithCodeSmithyMake("CodeSmithyUIImplementation", "Build/CodeSmithyIDE/CodeSmithy/UIImplementation/Makefiles/VC14/CodeSmithyUIImplementation.sln")
print("")

print("Step 16: Building CodeSmithy", flush=True)
buildWithCodeSmithyMake("CodeSmithy", "Build/CodeSmithyIDE/CodeSmithy/UI/Makefiles/VC14/CodeSmithy.sln")
print("")

print("Step 17: Building CodeSmithyCore tests", flush=True)
buildWithCodeSmithyMake("CodeSmithyCore", "Build/CodeSmithyIDE/CodeSmithy/Tests/Core/Makefiles/VC14/CodeSmithyCoreTests.sln")
print("")

print("Step 18: Building CodeSmithyMake tests", flush=True)
buildWithCodeSmithyMake("CodeSmithyMake", "Build/CodeSmithyIDE/CodeSmithy/Tests/Make/Makefiles/VC14/CodeSmithyMakeTests.sln")
print("")
