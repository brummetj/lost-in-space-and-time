"""Lost in Space and Time

Usage:
    lispat --path=<content-path> --convert
    lispat --path=<content-path> --train [--nn][--ss]
    lispat --input <input-string> --nn
    lispat [-h | --help]
    lispat --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --input       A simple word input
  --convert     Convert pdfs/docx files to txt
  --nn          Nearest Neighbor Algorithm
  --ss          Semantic Similarity

"""
import sys
import docopt
from lispat.base.manager import CommandManager
from lispat.utils.logger import Logger

logger = Logger("Main")


def main():

    try:
        # logging = Logger("Main")
        args = docopt.docopt(__doc__)
        manager = CommandManager()
        if args['--path']:
            user_path = args['--path']
            manager.create_path(user_path)

            if args['--convert']:
                manager.convert()
            if args['--train']:
                if args['--nn']:
                    manager.train('nn')
                if args['--ss']:
                    manager.train('ss')

    except KeyboardInterrupt:
        logger.getLogger().error("Keyboard interrupt. Exiting")
        sys.exit("Later")


if __name__ == '__main__':
    main()
