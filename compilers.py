import os.path
import subprocess

class Compiler:
    def __init__(self, name, short_name, executable):
        self.name = name
        self.short_name = short_name
        self.executable = executable

    def compile(self, makefile_path, input):
        try:
            subprocess.check_call([self.executable, makefile_path,
                                   "/build", "Debug"])
        except subprocess.CalledProcessError:
            launchIDE = input.query("    Compilation failed. Do you you want to launch the IDE? [y/n]", ["y", "n"])
            if launchIDE == "y":
                subprocess.Popen([self.executable, makefile_path])
            raise RuntimeError("Compilation of " + makefile_path + " failed.")


class Compilers:
    def __init__(self):
        self.compilers = []
        foundMSVC14 = os.path.isfile("C:/Program Files (x86)/Microsoft Visual Studio 14.0/Common7/IDE/devenv.exe")
        if foundMSVC14:
            self.compilers.append(Compiler("Visual Studio 2015", "VC14", "C:/Program Files (x86)/Microsoft Visual Studio 14.0/Common7/IDE/devenv.exe"))
        foundMSVC2017 = os.path.isfile("C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/Common7/IDE/devenv.exe")
        if foundMSVC2017:
            self.compilers.append(Compiler("Visual Studio 2017", "VC15", "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/Common7/IDE/devenv.exe"))

    def show_compiler_list(self):
        if len(self.compilers) != 0:
            print("    The following compilers have been found")
            for i, compiler in enumerate(self.compilers):
                print("        " + str(i+1) + ") " + compiler.name)
        else:
            print("    No compilers have been found")

    def find_by_name(self, name):
        for compiler in self.compilers:
            if compiler.name == name:
                return compiler
        return None
