from enum import Enum
from compilers import VisualStudio

class BuildTools:
    def __init__(self, cmake, compiler, codesmithymake):
        self.cmake = cmake
        self.compiler = compiler
        self.codesmithymake = codesmithymake


class BuildConfiguration:
    class VisualStudioConfigurationType(Enum):
        DEBUG = 1
        RELEASE = 2

    def __init__(self, selected_architecture, compiler_configuration):
        self.cmake_configuration = compiler_configuration
        self.compiler_configuration = compiler_configuration + "|"
        if selected_architecture == "64":
            self.compiler_configuration += "x64"
        else:
            self.compiler_configuration += "Win32"
        self.codesmithymake_configuration = "Microsoft Windows "
        if selected_architecture == "64":
            self.codesmithymake_configuration += "x86_64"
        else:
            self.codesmithymake_configuration += "x86"

    def select_configuration(compiler, input, state):
        compiler_configuration = None
        if isinstance(compiler, VisualStudio):
            if state.compiler_configuration == "":
                compiler_configuration = input.query("    Choose configuration.", ["Debug", "Release"], "Debug")
                state.set_compiler_configuration(compiler_configuration)
            else:
                compiler_configuration = state.compiler_configuration
                print("    Using previous selection: " + compiler_configuration)
        return compiler_configuration
