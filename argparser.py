import argparse

class ArgParser:
    def __init__(self):
        argParser = argparse.ArgumentParser(
            description='Do a bootstrap build of CodeSmithy.')
        argParser.add_argument('--non-interactive', action='store_true',
            help='run the script in non-interactive mode')
        self.args = argParser.parse_args()
