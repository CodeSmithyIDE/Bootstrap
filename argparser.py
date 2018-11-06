import argparse


class ArgParser:
    def __init__(self):
        self.argParser = argparse.ArgumentParser(
            description='Do a bootstrap build of CodeSmithy.')
        self.argParser.add_argument(
            '--non-interactive', action='store_true',
            help='run the script in non-interactive mode')

    def parse(self):
        return self.argParser.parse_args()
