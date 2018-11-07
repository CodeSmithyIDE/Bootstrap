import argparse


class ArgParser:
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(
            description='Do a bootstrap build of CodeSmithy.')
        self.arg_parser.add_argument(
            '--non-interactive', action='store_true',
            help='run the script in non-interactive mode')

    def parse(self):
        return self.arg_parser.parse_args()
