import os
import zipfile
import subprocess
import shutil
from pathlib import Path
from state import State
from output import Output
from build import BuildConfiguration


class CMake:
    """Wrapper used to invoke CMake."""

    def __init__(self, generator):
        self.generator = generator

    def install(self, platform_name: str, is64bit: bool, state: State,
                output: Output):
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
        state: State
            The state of the bootstrap build.
        output: Output
            The output helper.
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

    def build(self, makefile_path: str,
              build_configuration: BuildConfiguration,
              logfile: str):
        """Generate the makefiles and then use them to build the project.

        Parameters
        ----------
        makefile_path : str
            Path to the makefile. It should be the CMakeLists.txt.
        build_configuration: BuildConfiguration
            The build configuration.
        logfile: str
            The path to the file where the output of CMake will be written.
        """
        previous_working_dir = os.getcwd()
        os.chdir(Path(makefile_path).parent)
        try:
            with open(logfile, "w") as output_file:
                cmake_path = previous_working_dir + "/" + self.path
                generation_args = [cmake_path, "-G", self.generator, "."]
                generation_args.extend(build_configuration.cmake_generation_args)
                print("    Executing " + " ".join(generation_args))
                subprocess.check_call(generation_args, stdout=output_file)
                build_args = [cmake_path, "--build", ".", "--config",
                              build_configuration.cmake_configuration]
                print("    Executing " + " ".join(build_args))
                subprocess.check_call(build_args, stdout=output_file)
        except subprocess.CalledProcessError:
            raise RuntimeError("Compilation of " + makefile_path + " failed.")
        finally:
            os.chdir(previous_working_dir)

    def _install(self, platform_name, is64bit):
        self.path = ""
        if platform_name == "Windows":
            architecture_string = ""
            if is64bit:
                architecture_string = "-win64-x64"
            else:
                architecture_string = "-win32-x86"
            source_path = "CMake/cmake-3.12.3" + architecture_string + ".zip"
            zip_ref = zipfile.ZipFile(source_path, "r")
            self.path = "Build/cmake-3.12.3" + architecture_string + \
                        "/bin/cmake.exe"

            # TODO : the path we delete here doesn't seem right
            shutil.rmtree(self.path, ignore_errors=True)
            zip_ref.extractall("Build")
            zip_ref.close()
