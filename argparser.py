import argparse


class ArgParser:
    """Command line parser."""

    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(
            description='Do a bootstrap build of CodeSmithy.')
        self.arg_parser.add_argument(
            '--launch',
            help='launches a project inside an IDE or shell',
            metavar='PROJECTNAME')
        self.arg_parser.add_argument(
            '--non-interactive', action='store_true',
            help='run the script in non-interactive mode')
        self.arg_parser.add_argument(
            '--skip-downloads', action='store_true',
            help='skip the download of the packages')
        self.arg_parser.add_argument(
            '--skip-tests', action='store_true',
            help='skip the tests')

    def parse(self) -> argparse.Namespace:
        """Parse the command line.

        Returns
        -------
        argparse.Namespace
            A namespace instanced populated with the arguments.
        """
        return self.arg_parser.parse_args()
