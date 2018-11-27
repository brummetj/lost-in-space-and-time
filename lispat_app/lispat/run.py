"""Lost in Space and Time.

Usage:
    lispat --path=<content-path>  [--train] [--compare] [--convert]
    lispat --predict
    lispat [-h | --help]
    lispat --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --input       A simple word input
  --convert     Convert PDFs and DOCX files to TXT
  --compare     Submit a Document to be compared
  --train       Submit documents to be used for training data
  --predict     Submit a sentence to see what could be predicted

"""
import sys
import docopt
from lispat.base.manager import CommandManager
from lispat.utils.logger import Logger


logger = Logger("Main")


def main():

    try:
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
        if args['--predict']:
            manager.predict()

    except KeyboardInterrupt:
        logger.getLogger().error("Keyboard interrupt. Exiting")
        sys.exit(1)


if __name__ == '__main__':
    main()
