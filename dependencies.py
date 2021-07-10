import os


class Dependencies:
    def check(self, output):
        print("")
        output.print_step_title("Checking dependencies")
        if "ISHIKO_CPP_THIRD_PARTY_BOOST" not in os.environ:
            raise RuntimeError("Missing dependency: ISHIKO_CPP_THIRD_PARTY_BOOST environment variable"
                               " not set")
        else:
            print("    ISHIKO_CPP_THIRD_PARTY_BOOST: " + os.environ["ISHIKO_CPP_THIRD_PARTY_BOOST"])
        output.next_step()
