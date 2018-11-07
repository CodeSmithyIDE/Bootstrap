class Output:
    def __init__(self):
        self.current_step = 1

    def print_step_title(self, title):
        print("Step " + str(self.current_step )+ ": " + title, flush=True)

    def next_step(self):
        self.current_step += 1
