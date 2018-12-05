"""Lost in Space and Time

Usage:
    lispat analytics --path=<content-path>  [--train] [--compare] [--array] [--df] [-A]
    lispat compare --standard=<content-path> --submission=<content-path>
    lispat clean [--all]
    lispat [-h | --help]
    lispat --version

Options:

  -h --help                      Show this screen.
  --version                      Show version.

  Analytics:
    analytics                    A look at the data give, whether its a single doc or directory of docs.

    Args:
    --compare                    Submit a Document to be compared
    --train                   Submit documents to be used for training data
    --array                  processing data as an array
    --df                         processing data as a dataframe
    -A                           get all processed txt data.
    --path=<content-path>        process data from a single path. multiple docs or single docs

                Example: lispat analytics --path=<content-path> --train --array --df

  Comparisons:
    compare                      Compare a standard with a submission

    Args:
    --standard=<content-path>    a standard document to use for comparing against a submission
    --submission=<content-path>  a submission document to use for comparing against a standard.

                Example: lispat compare --standard=<content-path> --submission=<content_path>

  Utilities:
     clean                        remove data in local storage.
     --all                        remove all data in local storage.

"""
import docopt, sys, nltk
from lispat.base.manager import CommandManager
from lispat.utils.logger import Logger
from lispat.utils.colors import bcolors

import spacy

logger = Logger("Main")
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def main():

    try:
        args = docopt.docopt(__doc__)
        manager = CommandManager()
        if args['--path'] and args['analytics']:
            user_path = args['--path']
            manager.create_path(user_path)
            manager.run_analytics(args)

        if args['--standard'] and args['--submission']:
            std_path = args['--standard']
            sub_path = args['--submission']

        if args['clean']:
            manager.clean(args)

    except KeyboardInterrupt:
        logger.getLogger().error( bcolors.FAIL + "Keyboard interrupt. Exiting"  + bcolors.ENDC)
        sys.exit(1)

if __name__ == '__main__':
    main()
