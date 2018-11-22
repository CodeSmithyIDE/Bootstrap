class BuildTools:
    def __init__(self, cmake, compiler, codesmithymake):
        self.cmake = cmake
        self.compiler = compiler
        self.codesmithymake = codesmithymake


class BuildConfiguration:
    def __init__(self, cmake_configuration, compiler_configuration,
                 codesmithymake_configuration):
        self.cmake_configuration = cmake_configuration
        self.compiler_configuration = compiler_configuration
        self.codesmithymake_configuration = codesmithymake_configuration
