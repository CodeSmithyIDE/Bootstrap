import platform
import os
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
from compilers import VisualStudio
from codesmithymake import CodeSmithyMake
from build import BuildTools
from utils import Utils


def try_restore_previous_state(input, state):
    if state.previous_state_found:
        resume = input.query(
            "Previous execution detected. Do you want to resume it?",
            ["y", "n"], "n")
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
            selected_architecture = input.query("    Select architecture.", ["32", "64"], "64")
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
        compiler = compilers.select_compiler(input, state, output)

        if isinstance(compiler, VisualStudio):
            if state.compiler_configuration == "":
                compiler_configuration = input.query("    Choose configuration.", ["Debug", "Release"], "Debug")
                state.set_compiler_configuration(compiler_configuration)
            else:
                compiler_configuration = state.compiler_configuration
                print("    Using previous selection: " + compiler_configuration)

        cmake = CMake(compiler.cmake_generator)
        cmake.install(platform_name, (selected_architecture == "64"),
                      state, output)

        codesmithymake = CodeSmithyMake(selected_architecture)

        build_tools = BuildTools(cmake, compiler, codesmithymake)

        cmake_configuration = compiler_configuration
        
        compiler_configuration += "|"
        codesmithymake_configuration = "Microsoft Windows "
        if selected_architecture == "64":
            compiler_configuration += "x64"
            codesmithymake_configuration += "x86_64"
        else:
            compiler_configuration += "Win32"
            codesmithymake_configuration += "x86"
        
        projects.build(cmake_configuration,
                       build_tools, compiler_configuration,
                       codesmithymake_configuration,
                       input, state, output)

        print("")
        output.print_step_title("Running tests")
        if args.skip_tests:
            print("    Skipping tests")
        else:
            projects.test()
        output.next_step()

        print("")
        output.print_step_title("Setting up second-phase of bootstrap")
        second_phase_path = str(Path(os.getcwd()).parent) + \
                            "/SecondPhaseBootstrap"
        Path(second_phase_path).mkdir(exist_ok=True)
        print(second_phase_path)
        # TODO
        shutil.copyfile("Build/CodeSmithyIDE/CodeSmithy/Bin/x64/CodeSmithy.exe", second_phase_path + "/CodeSmithy.exe")
        output.next_step()
    except RuntimeError as error:
        print("")
        print("ERROR:", error)
        sys.exit(-1)

    codeSmithyMakePath = "Build/CodeSmithyIDE/CodeSmithy/Bin/Win32/CodeSmithyMake.exe"


def main_launch_project(args, input, state, output):
    projects = Projects()

    # TODO: restore state
    # TODO: this is broken, an argument is missing
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
