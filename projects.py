import re
from download import Downloader
from download import Download


class Project:
    def __init__(self, name, makefile_path):
        self.name = name
        self.makefile_path = "Build/" + name + "/" + makefile_path

    def build(self, cmake, compiler, output):
        print("")
        output.print_step_title("Building " + self.name)
        try:
            if self.makefile_path.endswith("/CMakeLists.txt"):
                log = self.name + "_build.log"
                print("    Using CMake, build log: " + log)
                cmake.compile(self.makefile_path, log)
            else:
                print("    Using " + compiler.name)
                resolved_makefile_path = re.sub(r"\$\(compiler_short_name\)",
                                                compiler.short_name,
                                                self.makefile_path)
                compiler.compile(resolved_makefile_path)
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

    def build(self, cmake, compiler, output):
        print("")
        output.print_step_title("Unzipping source packages")
        self.downloader.unzip()
        output.next_step()
        for project in self.projects:
            project.build(cmake, compiler, output)
