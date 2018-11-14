import argparse


class ArgParser:
    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(
            description='Do a bootstrap build of CodeSmithy.')
        self.arg_parser.add_argument(
            '--non-interactive', action='store_true',
            help='run the script in non-interactive mode')
        self.arg_parser.add_argument(
            '--skip-downloads', action='store_true',
            help='skip the download of the packages')

    def parse(self):
        return self.arg_parser.parse_args()
