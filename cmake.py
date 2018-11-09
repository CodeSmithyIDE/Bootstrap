import os
import zipfile
import subprocess
import shutil

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

    def compile(self):
        os.chdir("Build/libgit2")
        with open("../libgit2.log", "w") as output_file:
            rc = subprocess.call(["../../" + self.path, "."], stdout=output_file)
            rc = subprocess.call(["../../" + self.path, "--build", "."], stdout=output_file)
            if rc == 0:
                print("    libgit2 build successfully")
            else:
                print("    Failed to build libgit2, exiting")
                sys.exit(-1)
        os.chdir("../..")
