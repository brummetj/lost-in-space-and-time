"""Lost in Space and Time

Usage:
    lispat --path=<content-path> --train [--nn]
    lispat --input <input-string> --nn
    lispat [-h | --help]
    lispat --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --input       A simple word input
  --nn          Nearest Neighbor Algorithm

"""
<<<<<<< HEAD
import docopt
import time
=======
import docopt, sys
>>>>>>> develop
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

            if args['--train']:
                if args['--nn']:
                    manager.train('nn')

    except KeyboardInterrupt:
        logger.getLogger().error("Keyboard interrupt. Exiting")
        sys.exit("Later")



if __name__ == '__main__':
    main()
