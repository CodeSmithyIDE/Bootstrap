from typing import Optional
import os
import re
import subprocess
from download import Downloader
from download import Download
from build import BuildConfiguration


class Project:
    """Represents a project that can be downloaded and optionally built."""

    def __init__(self,
                 name: str,
                 env_var: str,
                 makefile_path: Optional[str],
                 use_codesmithy_make: bool):
        """
        Parameters
        ----------
        name : str
            The name of the project. The location of the package to download is
            derived from the name.
        env_var: str
            The name of the environment variable that will point to the
            location of this project. The location is derived from the name.
        makefile_path: str, optional
            The path of the makefile used to build the project. The path is
            relative to the directory where the project is unzipped. None if
            the project only needs to be downloaded.
        use_codesmithy_make: bool
            Whether CodeSmithyMake should be used to build the project.
        """

        self.name = name
        self.env_var = env_var
        if makefile_path is None:
            self.makefile_path = None
        else:
            self.makefile_path = "Build/" + name + "/" + makefile_path
        self.use_codesmithy_make = use_codesmithy_make

        split_name = name.split("/")

        # The installation directory is derived from the project name
        if len(split_name) == 1:
            self.install_dir = split_name[0]
        else:
            self.install_dir = split_name[0] + "/" + split_name[1]

        self.built = False

    def create_downloader(self) -> Downloader:
        """Creates a downloader to download the package(s) for this project.

        Returns
        -------
        Downloader
            An instance of the Downloader class that can be used to download the
            package or packages for this project.
        """

        downloader = Downloader()

        # The download URL is derived from the project name
        split_name = self.name.split("/")
        download = None
        if len(split_name) == 1:
            download_url = "https://github.com/CodeSmithyIDE/" + \
                           split_name[0] + "/archive/master.zip"
            download = Download(split_name[0], download_url)
        else:
            download_url = "https://github.com/CodeSmithyIDE/" + \
                           split_name[1] + "/archive/master.zip"
            download = Download(split_name[1], download_url, split_name[0])
        downloader.downloads.append(download)

        return downloader

    def unzip(self, downloader):
        split_name = self.name.split("/")
        if len(split_name) == 1:
            downloader.unzip(split_name[0])
        else:
            downloader.unzip(split_name[1])

    def build(self, build_tools, parent_build_configuration,
              input, output):
        try:
            if self.makefile_path is None:
                print("    No build required for this project")
            else:
                cmake = build_tools.cmake
                compiler = build_tools.compiler
                codesmithymake = build_tools.codesmithymake
                build_configuration = BuildConfiguration(parent_build_configuration)
                resolved_makefile_path = self._resolve_makefile_path(compiler)
                if not os.path.exists(resolved_makefile_path):
                    raise RuntimeError(resolved_makefile_path + " not found")
                if self.use_codesmithy_make:
                    print("    Using CodeSmithyMake")
                    codesmithymake.build(compiler, resolved_makefile_path,
                                         build_configuration.codesmithymake_configuration,
                                         input)
                elif self.makefile_path.endswith("/CMakeLists.txt"):
                    log = self.name + "_build.log"
                    print("    Using CMake, build log: " + log)
                    cmake.build(resolved_makefile_path, build_configuration,
                                log)
                else:
                    print("    Using " + compiler.name)
                    compiler.compile(resolved_makefile_path,
                                     build_configuration.compiler_configuration,
                                     input)
                print("    Project build successfully")
            self.built = True
        except RuntimeError:
            print("    Failed to build project")
            raise

    def launch(self, compiler):
        compiler.launch(self._resolve_makefile_path(compiler))

    def _resolve_makefile_path(self, compiler):
        return re.sub(r"\$\(compiler_short_name\)",
                      compiler.short_name,
                      self.makefile_path)


class wxWidgetsProject(Project):
    def __init__(self):
        super().__init__("wxWidgets", "WXWIN",
                         "build/msw/wx_$(compiler_short_name).sln", False)

    def create_downloader(self):
        downloader = super().create_downloader()
        downloader.downloads.append(
            Download("zlib",
                     "https://github.com/CodeSmithyIDE/zlib/archive/wx.zip",
                     None, "wx", "Build/wxWidgets/src"))
        downloader.downloads.append(
            Download("libpng",
                     "https://github.com/CodeSmithyIDE/libpng/archive/wx.zip",
                     None, "wx", "Build/wxWidgets/src"))
        downloader.downloads.append(
            Download("libexpat",
                     "https://github.com/CodeSmithyIDE/libexpat/archive/wx.zip",
                     None, "wx", "Build/wxWidgets/src"))
        downloader.downloads.append(
            Download("libjpeg-turbo",
                     "https://github.com/CodeSmithyIDE/libjpeg-turbo/archive/wx.zip",
                     None, "wx", "Build/wxWidgets/src"))
        downloader.downloads.append(
            Download("libtiff",
                     "https://github.com/CodeSmithyIDE/libtiff/archive/wx.zip",
                     None, "wx", "Build/wxWidgets/src"))
        return downloader

    def unzip(self, downloader):
        super().unzip(downloader)
        downloader.unzip("zlib")
        downloader.unzip("libpng")
        os.rmdir("Build/wxWidgets/src/png")
        os.rename("Build/wxWidgets/src/libpng", "Build/wxWidgets/src/png")
        downloader.unzip("libexpat")
        os.rmdir("Build/wxWidgets/src/expat")
        os.rename("Build/wxWidgets/src/libexpat", "Build/wxWidgets/src/expat")
        downloader.unzip("libjpeg-turbo")
        os.rmdir("Build/wxWidgets/src/jpeg")
        os.rename("Build/wxWidgets/src/libjpeg-turbo", "Build/wxWidgets/src/jpeg")
        downloader.unzip("libtiff")
        os.rmdir("Build/wxWidgets/src/tiff")
        os.rename("Build/wxWidgets/src/libtiff", "Build/wxWidgets/src/tiff")

    def _resolve_makefile_path(self, compiler):
        return re.sub(r"\$\(compiler_short_name\)",
                      compiler.short_name.lower(),
                      self.makefile_path)


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
            "Makefiles/$(compiler_short_name)/IshikoWindowsRegistry.sln",
            True))
        self.projects.append(Project(
            "Ishiko/FileTypes",
            "ISHIKO",
            "Makefiles/$(compiler_short_name)/IshikoFileTypes.sln",
            True))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/UICore",
            "CODESMITHY",
            "Makefiles/$(compiler_short_name)/CodeSmithyUICore.sln",
            True))
        self.projects.append(wxWidgetsProject())
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/UIElements",
            "CODESMITHY",
            "Makefiles/$(compiler_short_name)/CodeSmithyUIElements.sln",
            True))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/UIImplementation",
            "CODESMITHY",
            "Makefiles/$(compiler_short_name)/CodeSmithyUIImplementation.sln",
            True))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/UI",
            "CODESMITHY",
            "Makefiles/$(compiler_short_name)/CodeSmithy.sln",
            True))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/Tests/Core",
            "CODESMITHY",
            "Makefiles/$(compiler_short_name)/CodeSmithyCoreTests.sln",
            True))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/Tests/Make",
            "CODESMITHY",
            "Makefiles/$(compiler_short_name)/CodeSmithyMakeTests.sln",
            True))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/Tests/UICore",
            "CODESMITHY",
            "Makefiles/$(compiler_short_name)/CodeSmithyUICoreTests.sln",
            True))
        self.tests = []
        # TODO
        self.tests.append("Build/CodeSmithyIDE/CodeSmithy/Tests/Core/Makefiles/VC15/x64/Debug/CodeSmithyCoreTests")
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

    def build(self, build_tools, build_configuration,
              input, state, output):
        # For now only bypass pugixml, libgit2 and wxWidgets because they
        # are independent from the rest. More complex logic is required to
        # handle the other projects.
        # Unless we have built all project succesfully.
        for project in self.projects:
            if state.build_complete:
                project.built = True
            elif project.name in ["libgit2", "pugixml", "wxWidgets"]:
                if project.name in state.built_projects:
                    project.built = True
        for project in self.projects:
            print("")
            output.print_step_title("Building " + project.name)
            if project.built:
                print("    Using previous execution")
            else:
                project.unzip(self.downloader)
                project.build(build_tools, build_configuration,
                              input, output)
            state.set_built_project(project.name)
            output.next_step()
        state.set_build_complete()

    def test(self):
        for test in self.tests:
            # TODO
            subprocess.check_call([test])

    def _init_downloader(self):
        for project in self.projects:
            project_downloader = project.create_downloader()
            self.downloader.merge(project_downloader)
