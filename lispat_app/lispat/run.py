"""Lost in Space and Time

Usage:
    lispat --path=<content-path> [--nn]
    lispat --input <input-string> --nn
    lispat [-h | --help]
    lispat --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --input       A simple word input
  --nn          Nearest Neighbor Algorithm

"""
import docopt
import time
from lispat.base.manager import CommandManager


def main():
    # logging = Logger("Main")
    args = docopt.docopt(__doc__)
    manager = CommandManager()
    if args['--path']:
        user_path = args['--path']
        manager.create_path(user_path)

        if args['--nn']:
            manager.train('nn')



if __name__ == '__main__':
    main()
