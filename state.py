import json


class State:
    def __init__(self):
        self.reset_variables()
        try:
            with open('state.json', 'r') as file:
                state = json.loads(file.read())
                self.download_complete = state["download_complete"]
                self.selected_compiler = state["selected_compiler"]
                self.cmake_installed = state["cmake_installed"]
                self.previous_state_found = True
        except IOError:
            self.save()

    def reset(self):
        self.reset_variables()
        self.save()

    def set_download_complete(self):
        self.download_complete = True
        self.save()

    def set_selected_compiler(self, compiler):
        self.selected_compiler = compiler
        self.save()

    def save(self):
        with open('state.json', 'w+') as file:
            state = {"download_complete": self.download_complete,
                     "selected_compiler": self.selected_compiler,
                     "cmake_installed": self.cmake_installed}
            file.write(json.dumps(state))

    def reset_variables(self):
        self.previous_state_found = False
        self.download_complete = False
        self.selected_compiler = ""
        self.cmake_installed = False
