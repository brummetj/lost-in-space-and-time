"""Lost in Space and Time

Usage:
    lispat --path=<content-path>  [--train] [--compare] [--array] [--df]
    lispat [-h | --help]
    lispat --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --compare     Submit a Document to be compared
  --train       Submit documents to be used for training data
  --array       processing data as an array
  --df          processing data as a dataframe

"""
import docopt, sys, nltk
from lispat.base.manager import CommandManager
from lispat.utils.logger import Logger

import spacy

logger = Logger("Main")
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

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
