import os
import zipfile
import subprocess
import shutil
from pathlib import Path

class CMake:
    """Wrapper used to invoke CMake."""

    def __init__(self, generator):
        self.generator = generator

    def install(self, platform_name: str, is64bit: bool, state, output):
        """Installs CMake.

        CMake is not easily buildable on Windows so we rely on a binary
        distribution

        Parameters
        ----------
        platform_name : str
            The name of the platform. Used to detect whether we are running on
            Windows.
        is64bit: bool
            Whether to installed the 64-bit or 32-bit version CMake.
        """
        print("")
        output.print_step_title("Installing CMake")
        if state.cmake_path == "":
            self._install(platform_name, is64bit)
            print("    CMake installed successfully")
        else:
            self.path = state.cmake_path
            print("    Using previous installation: " + self.path)
        state.set_cmake_path(self.path)
        output.next_step()

    def compile(self, makefile_path, configuration, logfile):
        previous_working_dir = os.getcwd()
        os.chdir(Path(makefile_path).parent)
        try:
            with open(logfile, "w") as output_file:
                # TODO
                if makefile_path.find("libgit2") != -1:
                    subprocess.check_call(
                        [previous_working_dir + "/" + self.path, "-G", self.generator, ".", "-DBUILD_SHARED_LIBS=OFF", "-DSTATIC_CRT=OFF"],
                        stdout=output_file)
                else:
                    subprocess.check_call(
                        [previous_working_dir + "/" + self.path, "-G", self.generator, "."],
                        stdout=output_file)
                subprocess.check_call(
                    [previous_working_dir + "/" + self.path, "--build", ".", "--config", configuration],
                    stdout=output_file)
        except subprocess.CalledProcessError:
            raise RuntimeError("Compilation of " + makefile_path + " failed.")
        finally:
            os.chdir(previous_working_dir)

    def _install(self, platform_name, is64bit):
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
