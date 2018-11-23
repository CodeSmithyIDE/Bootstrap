from compilers import VisualStudio

class BuildTools:
    """Provides a way to group all the available build tools in one place."""

    def __init__(self, cmake, compiler, codesmithymake):
        self.cmake = cmake
        self.compiler = compiler
        self.codesmithymake = codesmithymake


class BuildConfiguration:
    """Unified configuration information for the build tools."""
    
    def __init__(self, build_configuration = None):
        if build_configuration is None:
            self.cmake_configuration = ""
            self.compiler_configuration = ""
            self.codesmithymake_configuration = ""
        else:
            self.cmake_configuration = build_configuration.cmake_configuration
            self.compiler_configuration = build_configuration.compiler_configuration
            self.codesmithymake_configuration = build_configuration.codesmithymake_configuration

    def select_configuration(self, architecture, compiler, input, state):
        compiler_configuration = self._select_compiler_configuration(compiler, input, state)
        self.cmake_configuration = compiler_configuration
        self.compiler_configuration = compiler_configuration + "|"
        if architecture == "64":
            self.compiler_configuration += "x64"
        else:
            self.compiler_configuration += "Win32"
        self.codesmithymake_configuration = "Microsoft Windows "
        if architecture == "64":
            self.codesmithymake_configuration += "x86_64"
        else:
            self.codesmithymake_configuration += "x86"

    def _select_compiler_configuration(self, compiler, input, state):
        compiler_configuration = None
        if isinstance(compiler, VisualStudio):
            if state.compiler_configuration == "":
                compiler_configuration = input.query("    Choose configuration.", ["Debug", "Release"], "Debug")
                state.set_compiler_configuration(compiler_configuration)
            else:
                compiler_configuration = state.compiler_configuration
                print("    Using previous selection: " + compiler_configuration)
        return compiler_configuration
