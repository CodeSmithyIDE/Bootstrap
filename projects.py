class Project:
    def __init__(self, name):
        self.name = name

    def build(self, compiler, output):
        print("")
        output.print_step_title("Building Process")
        processMakefilePath = "Build/Ishiko/Process/Makefiles/" + compiler.short_name + "/IshikoProcess.sln"
        rc = compiler.compile(processMakefilePath)
        if rc == 0:
            print("Process built successfully")
        else:
            print("Failed to build Process, exiting")
            sys.exit(-1)
        output.next_step()

class Projects:
    def __init__(self):
        self.projects = []
        self.projects.append(Project("Ishiko/Process"))

    def build(self, compiler, output):
        for project in self.projects:
            project.build(compiler, output)
