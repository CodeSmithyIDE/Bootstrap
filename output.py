import json


class Output:
    def __init__(self):
        self.current_step = 1
        with open('predefined_strings.json', 'r') as file:
            self.predefined_strings = json.loads(file.read())

    def print_predefined_string(self, string_id):
        print(self.predefined_strings[string_id])

    def print_main_title(self):
        title = self.predefined_strings["title"]
        print(title)
        print('-' * len(title))
        print("")

    def print_step_title(self, title):
        print("Step " + str(self.current_step )+ ": " + title, flush=True)

    def next_step(self):
        self.current_step += 1
