class Project:
    def __init__(self, name):
        self.name = name

    def build(self, compiler):
        print("Step 6: Building Process", flush=True)
        processMakefilePath = "Build/Ishiko/Process/Makefiles/" + compiler.short_name + "/IshikoProcess.sln"
        rc = compiler.compile(processMakefilePath)
        if rc == 0:
            print("Process built successfully")
        else:
            print("Failed to build Process, exiting")
            sys.exit(-1)
        print("")

class Projects:
    def __init__(self):
        self.projects = []
        self.projects.append(Project("Ishiko/Process"))

    def build(self, compiler):
        for project in self.projects:
            project.build(compiler)
