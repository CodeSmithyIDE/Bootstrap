from typing import Optional
import os
import re
from download import Downloader
from download import Download


class Project:
    """Represents a project that can be downloaded and optionally built."""

    def __init__(self, name: str, env_var: str, makefile_path: Optional[str]):
        """
        Parameters
        ----------
        name : str
            The name of the project. The location of the package to download is
            derived from the name.
        env_var: str
            The name of the environment variable that will point to the
            location of this project. The location is derived from the name.
        makefile_path : str, optional
            The path of the makefile used to build the project. None if the
            project only needs to be downloaded.
        """

        self.name = name
        self.env_var = env_var
        if makefile_path is None:
            self.makefile_path = None
        else:
            self.makefile_path = "Build/" + name + "/" + makefile_path

        # The installation directory is derived from the project name
        split_name = name.split("/")
        if len(split_name) == 1:
            self.install_dir = split_name[0]
        else:
            self.install_dir = split_name[0] + "/" + split_name[1]

    def build(self, cmake, compiler, input, output):
        print("")
        output.print_step_title("Building " + self.name)
        try:
            if self.makefile_path is None:
                print("    No build required for this project")
            elif self.makefile_path.endswith("/CMakeLists.txt"):
                log = self.name + "_build.log"
                print("    Using CMake, build log: " + log)
                cmake.compile(self.makefile_path, log)
                print("    Project build successfully")
            else:
                print("    Using " + compiler.name)
                resolved_makefile_path = re.sub(r"\$\(compiler_short_name\)",
                                                compiler.short_name,
                                                self.makefile_path)
                compiler.compile(resolved_makefile_path, input)
                print("    Project build successfully")
        except RuntimeError:
            print("    Failed to build project")
            raise
        finally:
            output.next_step()


class Projects:
    def __init__(self):
        self.downloader = Downloader()
        self.projects = []
        self.projects.append(Project(
            "pugixml",
            "PUGIXML",
            None))
        self.projects.append(Project(
            "libgit2",
            "LIBGIT2",
            "CMakeLists.txt"))
        self.projects.append(Project(
            "Ishiko/Process",
            "ISHIKO",
            "Makefiles/$(compiler_short_name)/IshikoProcess.sln"))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/Core",
            "CODESMITHY",
            "Makefiles/$(compiler_short_name)/CodeSmithyCore.sln"))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/Make",
            "CODESMITHY",
            "Makefiles/$(compiler_short_name)/CodeSmithyMake.sln"))
        self._init_downloader()

    def set_environment_variables(self, output):
        print("")
        output.print_step_title("Setting environment variables")
        env = {}
        for project in self.projects:
            value = os.getcwd() + "/Build/" + project.name.split("/")[0]
            if project.env_var in env:
                old_value = env[project.env_var]
                if (old_value != value):
                    exception_text = "Conflicting values for " + \
                        "environment variable " + project.env_var + " (" + \
                        value + " vs " + old_value + ")"
                    raise RuntimeError(exception_text)
            else:
                env[project.env_var] = value
        for var_name in env:
            print("    " + var_name + ": " + env[var_name])
            os.environ[var_name] = env[var_name]
        output.next_step()

    def download(self):
        self.downloader.download()

    def build(self, cmake, compiler, input, state, output):
        print("")
        output.print_step_title("Unzipping source packages")
        self.downloader.unzip()
        output.next_step()
        for project in self.projects:
            project.build(cmake, compiler, input, output)
            state.set_built_project(project.name)

    def _init_downloader(self):
        package_names = set()
        for project in self.projects:
            download = None
            package_names.add(project.install_dir)
        for package_name, i in zip(package_names, range(ord("a"), ord("z"))):
            download = None
            split_name = package_name.split("/")
            if len(split_name) == 1:
                download = Download(split_name[0])
            else:
                download = Download(split_name[1], split_name[0])
            self.downloader.downloads.append(download)

