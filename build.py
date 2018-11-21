class BuildTools:
    def __init__(self, cmake, compiler, codesmithymake):
        self.cmake = cmake
        self.compiler = compiler
        self.codesmithymake = codesmithymake


class BuildConfiguration:
    def __init__(self, compiler_configuration):
        self.compiler_configuration = compiler_configuration
