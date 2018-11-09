import os
import zipfile
import subprocess
import shutil
from pathlib import Path

class CMake:
    def __init__self(self):
        pass

    def install(self, platform_name, is64bit):
        self.path = ""
        if platform_name == "Windows":
            if is64bit:
                zip_ref = zipfile.ZipFile("CMake/cmake-3.12.3-win64-x64.zip", "r")
                self.path = "Build/cmake-3.12.3-win64-x64/bin/cmake.exe"
            else:
                zip_ref = zipfile.ZipFile("CMake/cmake-3.12.3-win32-x86.zip", "r")
                self.path = "Build/cmake-3.12.3-win32-x86/bin/cmake.exe"
            shutil.rmtree(self.path, ignore_errors=True)
            zip_ref.extractall("Build")
            zip_ref.close()

    def compile(self, makefile_path, logfile):
        previous_working_dir = os.getcwd()
        os.chdir(Path(makefile_path).parent)
        rc = 0
        with open(logfile, "w") as output_file:
            rc = subprocess.call(
                [previous_working_dir + "/" + self.path, "."],
                stdout=output_file)
            if rc == 0:
                rc = subprocess.call(
                    [previous_working_dir + "/" + self.path, "--build", "."],
                    stdout=output_file)
        os.chdir(previous_working_dir)
        return rc
