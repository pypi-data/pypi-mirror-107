import sys
import argparse
from os.path import abspath, dirname


sys.path.insert(0, abspath(dirname(abspath(__file__)) + '/..'))
from app import __version__


class Main:
    def __init__(self):
        super(Main, self).__init__()

    def is_even(self, number):
        return number % 2 == 0

    def run(self):
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="App")
    parser.add_argument('-v', '--version', action='version',
                        version='v{}'.format(__version__))

    args = parser.parse_args()
    if len(sys.argv) <= 1:
        parser.print_help()

    main = Main()
    main.run()
