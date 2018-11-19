import platform
import sys
import subprocess
from pathlib import Path
from input import Input
from output import Output
from argparser import ArgParser
from state import State
from dependencies import Dependencies
from projects import Projects
from cmake import CMake
from compilers import Compilers
from compilers import VisualStudio
from codesmithymake import CodeSmithyMake
from utils import Utils


def try_restore_previous_state(input, state):
    if state.previous_state_found:
        resume = input.query(
            "Previous execution detected. Do you want to resume it? [y/n]",
            ["y", "n"])
        if resume == "n":
            state.reset()
            Utils.rmdir_with_retry("Build", input)


def download_source_packages(projects, skip, input, state, output):
    print("")
    output.print_step_title("Downloading source packages")
    if skip:
        print("    Skipping downloads")
    elif not state.download_complete:
        Utils.rmdir_with_retry("Downloads", input)
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


def main_bootstrap_build(args, input, state, output):
    print("")
    output.print_main_title()

    try_restore_previous_state(input, state)

    platform_name = platform.system()
    is_64bit_supported = (platform.machine() == "AMD64")

    print("")
    output.print_step_title("Architecture choice")
    print("    Platform: " + platform_name)
    selected_architecture = ""
    if state.architecture == "":
        if is_64bit_supported:
            selected_architecture = input.query("    Select architecture. [32/64]", ["32", "64"])
        else:
            print("    Only 32-bit build supported")
            selected_architecture = "32"
    else:
        selected_architecture = state.architecture
        print("    Using previous selection: " + selected_architecture)
    state.set_architecture(selected_architecture)
    output.next_step()

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

    download_source_packages(projects, args.skip_downloads, input,
                             state, output)

    try:
        compilers = Compilers(selected_architecture)
        compiler = select_compiler(compilers, input, state, output)

        if isinstance(compiler, VisualStudio):
            if state.compiler_configuration == "":
                compiler_configuration = input.query("    Choose configuration. [Debug/Release]", ["Debug", "Release"])
                state.set_compiler_configuration(compiler_configuration)
            else:
                compiler_configuration = state.compiler_configuration
                print("    Using previous selection: " + compiler_configuration)

        cmake = CMake(compiler.cmake_generator)
        install_cmake(cmake, platform_name, (selected_architecture == "64"),
                      state, output)

        codesmithymake = CodeSmithyMake(selected_architecture)

        cmake_configuration = compiler_configuration
        
        compiler_configuration += "|"
        codesmithymake_configuration = "Microsoft Windows "
        if selected_architecture == "64":
            compiler_configuration += "x64"
            codesmithymake_configuration += "x86_64"
        else:
            compiler_configuration += "Win32"
            codesmithymake_configuration += "x86"
        
        projects.build(cmake, cmake_configuration,
                       compiler, compiler_configuration,
                       codesmithymake, codesmithymake_configuration,
                       input, state, output)

        if not args.skip_tests:
            projects.test()
    except RuntimeError as error:
        print("")
        print("ERROR:", error)
        sys.exit(-1)

    codeSmithyMakePath = "Build/CodeSmithyIDE/CodeSmithy/Bin/Win32/CodeSmithyMake.exe"


def main_launch_project(args, input, state, output):
    projects = Projects()

    compilers = Compilers()
    compiler = select_compiler(compilers, input, state, output)

    projects.get(args.launch).launch(compiler)


def main():
    args = ArgParser().parse()

    input = Input()
    output = Output()
    state = State()

    if args.launch is None:
        main_bootstrap_build(args, input, state, output)
    else:
        try:
            main_launch_project(args, input, state, output)
        except RuntimeError as error:
            print("")
            print("ERROR:", error)
            sys.exit(-1)


main()
