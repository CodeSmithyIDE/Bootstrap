import os
import subprocess

class CodeSmithyMake:
    def __init__(self):
        self.executable = os.getcwd() + "/Build/CodeSmithyIDE/CodeSmithy/Bin/Win32/CodeSmithyMake.exe"

    def build(self, compiler, makefile_path, input):
        try:
            subprocess.check_call([self.executable, makefile_path])
        except subprocess.CalledProcessError:
            launchIDE = input.query("    Compilation failed. Do you you want to launch the IDE? [y/n]", ["y", "n"])
            if launchIDE == "y":
                compiler.launch(makefile_path)
            raise RuntimeError("Compilation of " + makefile_path + " failed.")
