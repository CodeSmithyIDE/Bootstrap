import json


class State:
    def __init__(self):
        self.reset_variables()
        try:
            with open('state.json', 'r') as file:
                state = json.loads(file.read())
                self.architecture = state["architecture"]
                self.download_complete = state["download_complete"]
                self.selected_compiler = state["selected_compiler"]
                self.compiler_configuration = state["compiler_configuration"]
                self.cmake_path = state["cmake_path"]
                built_projects_list = state["built_projects"]
                for project in built_projects_list:
                    self.built_projects.add(project)
                self.build_complete = state["build_complete"]
                self.previous_state_found = True
        except IOError:
            self.save()

    def reset(self):
        self.reset_variables()
        self.save()

    def set_architecture(self, architecture):
        self.architecture = architecture
        self.save()

    def set_download_complete(self):
        self.download_complete = True
        self.save()

    def set_selected_compiler(self, compiler):
        self.selected_compiler = compiler
        self.save()

    def set_compiler_configuration(self, configuration):
        self.compiler_configuration = configuration
        self.save()

    def set_cmake_path(self, path):
        self.cmake_path = path
        self.save()

    def set_built_project(self, project):
        self.built_projects.add(project)
        self.save()

    def set_build_complete(self):
        self.build_complete = True
        self.save()

    def save(self):
        with open('state.json', 'w+') as file:
            built_projects_list = []
            for project in self.built_projects:
                built_projects_list.append(project)
            state = {"architecture": self.architecture,
                     "download_complete": self.download_complete,
                     "selected_compiler": self.selected_compiler,
                     "compiler_configuration": self.compiler_configuration,
                     "cmake_path": self.cmake_path,
                     "built_projects": built_projects_list,
                     "build_complete": self.build_complete}
            file.write(json.dumps(state))

    def reset_variables(self):
        self.previous_state_found = False
        self.architecture = ""
        self.download_complete = False
        self.selected_compiler = ""
        self.compiler_configuration = ""
        self.cmake_path = ""
        self.built_projects = set()
        self.build_complete = False
