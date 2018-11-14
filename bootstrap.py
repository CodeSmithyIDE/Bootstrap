import platform
import sys
import subprocess
import shutil
from pathlib import Path
from input import Input
from output import Output
from argparser import ArgParser
from state import State
from dependencies import Dependencies
from projects import Projects
from cmake import CMake
from compilers import Compilers
from codesmithymake import CodeSmithyMake


def try_restore_previous_state(input, state):
    if state.previous_state_found:
        resume = input.query(
            "Previous execution detected. Do you want to resume it? [y/n]",
            ["y", "n"])
        if resume == "n":
            state.reset()
            shutil.rmtree("Build", ignore_errors=True)


def download_source_packages(projects, skip, state, output):
    print("")
    output.print_step_title("Downloading source packages")
    if skip:
        print("    Skipping downloads")
    elif not state.download_complete:
        shutil.rmtree("Downloads", ignore_errors=True)
        projects.download()
    else:
        print("    Using previous execution")
    state.set_download_complete()
    output.next_step()


def select_compiler(compilers, input, state, output):
    print("")
    output.print_step_title("Finding compilers")
    compiler = None
    if state.selected_compiler == "":
        compilers.show_compiler_list()
        if len(compilers.compilers) == 0:
            print("")
            raise RuntimeError("No compilers found")
        valid_answers = []
        for i in range(1, len(compilers.compilers) + 1):
            valid_answers.append(str(i))
        answer = input.query("    Select the compiler to use:", valid_answers)
        selected_compiler_index = (int(answer) - 1)
        compiler = compilers.compilers[selected_compiler_index]
    else:
        compiler = compilers.find_by_name(state.selected_compiler)
        print("    Using previous selection: " + compiler.name)
    state.set_selected_compiler(compiler.name)
    output.next_step()
    return compiler


def install_cmake(cmake, platform_name, is64bit, state, output):
    # CMake is not easily buildable on Windows so we rely on a binary
    # distribution
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


def main():
    input = Input()
    output = Output()
    args = ArgParser().parse()
    state = State()

    print("")
    output.print_main_title()
    
    try_restore_previous_state(input, state)

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

    try:
        dependencies = Dependencies()
        dependencies.check(output)
        
        projects = Projects()
        
        projects.set_environment_variables(output)
    except RuntimeError as error:
        print("")
        print("ERROR:", error)
        sys.exit(-1)

    download_source_packages(projects, args.skip_downloads, state, output)

    try:
        compilers = Compilers()
        compiler = select_compiler(compilers, input, state, output)

        cmake = CMake(compiler.cmake_generator)
        install_cmake(cmake, platform_name, is64bit, state, output)

        codesmithymake = CodeSmithyMake()
        
        projects.build(cmake, compiler, codesmithymake, input, state, output)
    except RuntimeError as error:
        print("")
        print("ERROR:", error)
        sys.exit(-1)

    codeSmithyMakePath = "Build/CodeSmithyIDE/CodeSmithy/Bin/Win32/CodeSmithyMake.exe"


main()


def buildWithCodeSmithyMake(name, makefile):
    rc = subprocess.call([codeSmithyMakePath, makefile])
    if rc == 0:
        print(name + " built successfully")
    else:
        print("Failed to build " + name + ", exiting")
        sys.exit(-1)
    return


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
