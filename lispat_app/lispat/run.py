"""Lost in Space and Time

Usage:
    lispat --path=<content-path>  [--train] [--compare]
    lispat [-h | --help]
    lispat --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --input       A simple word input
  --compare     Submit a Document to be compared
  --train       Submit documents to be used for training data

"""
import sys
import docopt
import time
from lispat.base.manager import CommandManager

import spacy

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
                manager.run('train')
            if args['--compare']:
                manager.run('compare')

    except KeyboardInterrupt:
        logger.getLogger().error("Keyboard interrupt. Exiting")
        sys.exit(1)


if __name__ == '__main__':
    main()
