from typing import Optional
import os
import re
from download import Downloader
from download import Download


class Project:
    """Represents a project that can be downloaded and optionally built."""

    def __init__(self,
                 name: str,
                 env_var: str,
                 makefile_path: Optional[str],
                 use_codesmithy_make):
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
        self.use_codesmithy_make = use_codesmithy_make

        split_name = name.split("/")

        # The download URL is derived from the project name
        if len(split_name) == 1:
            self.download_url = "https://github.com/CodeSmithyIDE/" + \
                                split_name[0] + "/archive/master.zip"
        else:
            self.download_url = "https://github.com/CodeSmithyIDE/" + \
                                split_name[1] + "/archive/master.zip"

        # The installation directory is derived from the project name
        if len(split_name) == 1:
            self.install_dir = split_name[0]
        else:
            self.install_dir = split_name[0] + "/" + split_name[1]

        self.built = False

    def build(self, cmake, compiler, codesmithymake, input, output):
        try:
            if self.makefile_path is None:
                print("    No build required for this project")
            elif self.use_codesmithy_make:
                print("    Using CodeSmithyMake")
                resolved_makefile_path = re.sub(r"\$\(compiler_short_name\)",
                                                compiler.short_name,
                                                self.makefile_path)
                codesmithymake.build(compiler, resolved_makefile_path, input)
                print("    Project build successfully")
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
            self.built = True
        except RuntimeError:
            print("    Failed to build project")
            raise

    def launch(self, compiler):
        resolved_makefile_path = re.sub(r"\$\(compiler_short_name\)",
                                                compiler.short_name,
                                                self.makefile_path)
        compiler.launch(resolved_makefile_path)


class Projects:
    def __init__(self):
        self.downloader = Downloader()
        self.projects = []
        self.projects.append(Project(
            "pugixml",
            "PUGIXML",
            None,
            False))
        self.projects.append(Project(
            "libgit2",
            "LIBGIT2",
            "CMakeLists.txt",
            False))
        self.projects.append(Project(
            "Ishiko/Process",
            "ISHIKO",
            "Makefiles/$(compiler_short_name)/IshikoProcess.sln",
            False))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/Core",
            "CODESMITHY",
            "Makefiles/$(compiler_short_name)/CodeSmithyCore.sln",
            False))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/Make",
            "CODESMITHY",
            "Makefiles/$(compiler_short_name)/CodeSmithyMake.sln",
            False))
        self.projects.append(Project(
            "Ishiko/Errors",
            "ISHIKO",
            "Makefiles/$(compiler_short_name)/IshikoErrors.sln",
            True))
        self.projects.append(Project(
            "Ishiko/TestFramework/Core",
            "ISHIKO",
            "Makefiles/$(compiler_short_name)/IshikoTestFrameworkCore.sln",
            True))
        self.projects.append(Project(
            "Ishiko/WindowsRegistry",
            "ISHIKO",
            "IshikoWindowsRegistry",
            True))
        self.projects.append(Project(
            "Ishiko/FileTypes",
            "ISHIKO",
            "IshikoFileTypes",
            True))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/UICore",
            "CODESMITHY",
            "CodeSmithyUICore",
            True))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/UIElements",
            "CODESMITHY",
            "CodeSmithyUIElements",
            True))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/UIImplementation",
            "CODESMITHY",
            "CodeSmithyUIImplementation",
            True))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/UI",
            "CODESMITHY",
            "CodeSmithy",
            True))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/Tests/Core",
            "CODESMITHY",
            "CodeSmithyCoreTests",
            True))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/Tests/Make",
            "CODESMITHY",
            "CodeSmithyMakeTests",
            True))
      #  self.downloads.append(Download("wxWidgets", "TODO"))      
        self._init_downloader()

    def get(self, name):
        for project in self.projects:
            if project.name == name:
                return project
        return None

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

    def build(self, cmake, compiler, codesmithymake, input, state, output):
        # for now only bypass pugixml and libgit2 as more complex logic
        # is required to handle the other projects
        for project in self.projects:
            if project.name == "libgit2" or project.name == "pugixml":
                if project.name in state.built_projects:
                    project.built = True
        for project in self.projects:
            print("")
            output.print_step_title("Building " + project.name)
            if project.built:
                print("    Using previous execution")
            else:
                split_name = project.name.split("/")
                if len(split_name) == 1:
                    self.downloader.unzip(split_name[0])
                else:
                    self.downloader.unzip(split_name[1])
                project.build(cmake, compiler, codesmithymake, input, output)
            state.set_built_project(project.name)
            output.next_step()

    def _init_downloader(self):
        download_urls = {}
        for project in self.projects:
            download_urls[project.download_url] = project
        for download_url, project in download_urls.items():
            download = None
            split_name = project.name.split("/")
            if len(split_name) == 1:
                download = Download(split_name[0], download_url)
            else:
                download = Download(split_name[1], download_url, split_name[0])
            self.downloader.downloads.append(download)
