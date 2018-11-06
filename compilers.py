import os.path

class Compilers:
    def __init__(self):
        self.compilers = []
        self.compilerPaths = []
        foundMSVC14 = os.path.isfile("C:/Program Files (x86)/Microsoft Visual Studio 14.0/Common7/IDE/devenv.exe")
        if foundMSVC14:
            self.compilers.append("Visual Studio 2015")
            self.compilerPaths.append("C:/Program Files (x86)/Microsoft Visual Studio 14.0/Common7/IDE/devenv.exe")
        foundMSVC2017 = os.path.isfile("C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/Common7/IDE/devenv.exe")
        if foundMSVC2017:
            self.compilers.append("Visual Studio 2017")
            self.compilerPaths.append("C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/Common7/IDE/devenv.exe")

    def showCompilerList(self):
        if len(self.compilers) != 0:
            print("    The following compilers have been found")
            for i, compiler in enumerate(self.compilers):
                print("        " + str(i+1) + ") " + compiler)
        else:
            print("    No compilers have been found")
