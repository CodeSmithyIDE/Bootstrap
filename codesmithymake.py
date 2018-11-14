import os
import subprocess

class CodeSmithyMake:
    def __init__(self):
        self.executable = os.getcwd() + "/Build/CodeSmithyIDE/CodeSmithy/Bin/Win32/CodeSmithyMake.exe"

    def build(self, makefile_path):
        try:
            subprocess.check_call([self.executable, makefile_path])
        except subprocess.CalledProcessError:
            raise RuntimeError("Compilation of " + makefile_path + " failed.")
