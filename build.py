class BuildTools:
    def __init__(self, cmake, compiler, codesmithymake):
        self.cmake = cmake
        self.compiler = compiler
        self.codesmithymake = codesmithymake


class BuildConfiguration:
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
