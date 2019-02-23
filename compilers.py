import os.path
import subprocess


class Compiler:
    def __init__(self, name, short_name, executable, cmake_generator):
        self.name = name
        self.short_name = short_name
        self.executable = executable
        self.cmake_generator = cmake_generator

    def compile(self, makefile_path, configuration, input):
        try:
            subprocess.check_call([self.executable, makefile_path,
                                   "/build", configuration])
        except subprocess.CalledProcessError:
            raise RuntimeError("Compilation of " + makefile_path + " failed.")


class GNUmake(Compiler):
    def __init__(self):
        super().__init__("GNUmake", "GNUmakefile", "make", "")


class VisualStudio(Compiler):
    def __init__(self, name, short_name, executable, architecture):
        cmake_generator = ""
        if short_name == "VC14":
            cmake_generator = "Visual Studio 14 2015"
        elif short_name == "VC15":
            cmake_generator = "Visual Studio 15 2017"
        if architecture == "64":
            cmake_generator += " Win64"
        super().__init__(name, short_name, executable, cmake_generator)

    def compile(self, makefile_path, configuration, input):
        try:
            super().compile(makefile_path, configuration, input)
        except RuntimeError:
            launchIDE = input.query("    Compilation failed. Do you you want to launch the IDE?", ["y", "n"], "n")
            if launchIDE == "y":
                self.launch(makefile_path)
            raise

    def launch(self, makefile_path):
        subprocess.Popen([self.executable, makefile_path])


class Compilers:
    def __init__(self, target):
        self.architecture = target.architecture
        self.compilers = []
        foundMSVC2017 = os.path.isfile("C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/Common7/IDE/devenv.exe")
        if foundMSVC2017:
            self.compilers.append(VisualStudio("Visual Studio 2017", "VC15", "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/Common7/IDE/devenv.exe", self.architecture))
        foundMSVC14 = os.path.isfile("C:/Program Files (x86)/Microsoft Visual Studio 14.0/Common7/IDE/devenv.exe")
        if foundMSVC14:
            self.compilers.append(VisualStudio("Visual Studio 2015", "VC14", "C:/Program Files (x86)/Microsoft Visual Studio 14.0/Common7/IDE/devenv.exe", self.architecture))
        if target.platform == "Linux":
            self.compilers.append(GNUmake())
        

    def select_compiler(self, input, state, output):
        print("")
        output.print_step_title("Finding compilers")
        compiler = None
        if state.selected_compiler == "":
            self._show_compiler_list()
            if len(self.compilers) == 0:
                print("")
                raise RuntimeError("No compilers found")
            valid_answers = []
            for i in range(1, len(self.compilers) + 1):
                valid_answers.append(str(i))
            answer = input.query("    Select the compiler to use:", valid_answers, "1")
            selected_compiler_index = (int(answer) - 1)
            compiler = self.compilers[selected_compiler_index]
        else:
            compiler = self._find_by_name(state.selected_compiler)
            print("    Using previous selection: " + compiler.name)
        state.set_selected_compiler(compiler.name)
        output.next_step()
        return compiler

    def _show_compiler_list(self):
        if len(self.compilers) != 0:
            print("    The following compilers have been found")
            for i, compiler in enumerate(self.compilers):
                print("        " + str(i+1) + ") " + compiler.name)
        else:
            print("    No compilers have been found")

    def _find_by_name(self, name):
        for compiler in self.compilers:
            if compiler.name == name:
                return compiler
        return None
