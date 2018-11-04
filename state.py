import json

class State:
    def __init__(self):
        self.previousStateFound = False
        self.downloadComplete = False
        try:
            with open('state.json', 'r') as file:
                state = json.loads(file.read())
                self.downloadComplete = state["downloadComplete"]
                self.previousStateFound = True
        except:
            self.save()

    def reset(self):
        self.previousStateFound = False
        self.downloadComplete = False
        self.save()

    def setDownloadComplete(self):
        self.downloadComplete = True
        self.save()

    def save(self):
        with open('state.json', 'w+') as file:
            state = { "downloadComplete": self.downloadComplete }
            file.write(json.dumps(state))
