import json


class State:
    def __init__(self):
        self.previous_state_found = False
        self.download_complete = False
        try:
            with open('state.json', 'r') as file:
                state = json.loads(file.read())
                self.download_complete = state["download_complete"]
                self.previous_state_found = True
        except IOError:
            self.save()

    def reset(self):
        self.previous_state_found = False
        self.download_complete = False
        self.save()

    def set_download_complete(self):
        self.download_complete = True
        self.save()

    def save(self):
        with open('state.json', 'w+') as file:
            state = {"download_complete": self.download_complete}
            file.write(json.dumps(state))
