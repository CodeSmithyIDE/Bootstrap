from typing import Optional
import re
from download import Downloader
from download import Download


class Project:
    """Represents a project that can be downloaded and optionally built."""

    def __init__(self, name: str, makefile_path: Optional[str]):
        """
        Parameters
        ----------
        name : str
            The name of the project. The location of the package to download is
            derived from the name.
        makefile_path : str, optional
            The path of the makefile used to build the project. None if the
            project only needs to be downloaded.
        """

        self.name = name
        if makefile_path is None:
            self.makefile_path = None
        else:
            self.makefile_path = "Build/" + name + "/" + makefile_path

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
            None))
        self.projects.append(Project(
            "libgit2",
            "CMakeLists.txt"))
        self.projects.append(Project(
            "Ishiko/Process",
            "Makefiles/$(compiler_short_name)/IshikoProcess.sln"))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/Core",
            "Makefiles/$(compiler_short_name)/CodeSmithyCore.sln"))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/Make",
            "Makefiles/$(compiler_short_name)/CodeSmithyMake.sln"))
        package_names = set()
        for project in self.projects:
            split_name = project.name.split("/")
            download = None
            if len(split_name) == 1:
                package_names.add(split_name[0])
            else:
                package_names.add(split_name[0] + "/" + split_name[1])
        for package_name, i in zip(package_names, range(ord("a"), ord("z"))):
            download = None
            split_name = package_name.split("/")
            if len(split_name) == 1:
                download = Download(split_name[0])
            else:
                download = Download(split_name[1], split_name[0])
            self.downloader.downloads.append(download)

    def download(self):
        self.downloader.download()

    def build(self, cmake, compiler, input, output):
        print("")
        output.print_step_title("Unzipping source packages")
        self.downloader.unzip()
        output.next_step()
        for project in self.projects:
            project.build(cmake, compiler, input, output)
