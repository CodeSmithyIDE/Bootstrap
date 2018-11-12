import os

class Dependencies:
    def check(self):
        if "BOOST" not in os.environ:
            raise RuntimeError("Missing dependency: BOOST environment variable not set")
