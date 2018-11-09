import re


class Project:
    def __init__(self, name, makefile_path):
        self.name = name
        self.makefile_path = makefile_path

    def build(self, cmake, compiler, output):
        print("")
        output.print_step_title("Building " + self.name)
        try:
            if self.makefile_path.endswith("/CMakeLists.txt"):
                self.build_with_cmake(cmake)
            else:
                self.build_with_compiler(compiler)
        finally:
            output.next_step()

    def build_with_cmake(self, cmake):
        cmake.compile(self.makefile_path)

    def build_with_compiler(self, compiler):
        resolved_makefile_path = re.sub(r"\$\(compiler_short_name\)", compiler.short_name, self.makefile_path)
        rc = compiler.compile(resolved_makefile_path)
        if rc == 0:
            print("    Project built successfully")
        else:
            print("    Failed to build project, exiting")
            raise RuntimeError("Compilation error")


class Projects:
    def __init__(self):
        self.projects = []
        self.projects.append(Project(
            "libgit2",
            "Build/libgit2/CMakeLists.txt"))
        self.projects.append(Project(
            "Ishiko/Process",
            "Build/Ishiko/Process/Makefiles/$(compiler_short_name)/IshikoProcess.sln"))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/Core",
            "Build/CodeSmithyIDE/CodeSmithy/Core/Makefiles/$(compiler_short_name)/CodeSmithyCore.sln"))
        self.projects.append(Project(
            "CodeSmithyIDE/CodeSmithy/Make",
            "Build/CodeSmithyIDE/CodeSmithy/Core/Makefiles/$(compiler_short_name)/CodeSmithyMake.sln"))

    def build(self, cmake, compiler, output):
        for project in self.projects:
            project.build(cmake, compiler, output)
