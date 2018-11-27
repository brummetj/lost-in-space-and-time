"""Lost in Space and Time.

Usage:
    lispat --path=<content-path>  [--train] [--compare] [--array] [--df]
                                  [--convert]
    lispat [-h | --help]
    lispat --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --convert     Submit Documents to be converted
  --compare     Submit a Document to be compared
  --train       Submit documents to be used for training data
  --array       processing data as an array
  --df          processing data as a dataframe

"""

import sys
import nltk
import docopt
from lispat.utils.logger import Logger
from lispat.base.manager import CommandManager


logger = Logger("Main")


def main():

    try:
        args = docopt.docopt(__doc__)
        manager = CommandManager()
        if args['--path']:
            user_path = args['--path']
            manager.create_path(user_path)
            manager.run(args)

    except KeyboardInterrupt:
        logger.getLogger().error("Keyboard interrupt. Exiting")
        sys.exit(1)


if __name__ == '__main__':
    main()
