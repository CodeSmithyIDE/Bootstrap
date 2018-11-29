import os


class Dependencies:
    def check(self, output):
        print("")
        output.print_step_title("Checking dependencies")
        if "BOOST" not in os.environ:
            raise RuntimeError("Missing dependency: BOOST environment variable"
                               " not set")
        else:
            print("    BOOST: " + os.environ["BOOST"])
        output.next_step()
