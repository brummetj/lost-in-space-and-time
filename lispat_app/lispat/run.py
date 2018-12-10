"""Lost in Space and Time.

Usage:
    lispat analytics --path=<content-path>  [--train] [--compare] [--array] [--df] [--sp] [-A]
    lispat compare --standard=<content-path> --submission=<content-path> [--clean] [--empath] [--gitc] [--character] [--nn]
    lispat compare input --standard=<content-path> --text=<text> --nn
    lispat clean [--all]
    lispat [-h | --help]
    lispat --version

Options:

  -h --help                      Show this screen.
  --version                      Show version.

  Analytics:
    analytics                    A look at the data given, whether its a single doc or directory of docs.

    Args:
    --compare                    Submit a Document to be compared
    --train                      Submit documents to be used for training data
    --array                      Processing data as an array
    --df                         Processing data as a dataframe
    --sp                         Get semantic properties
    -A                           Get all processed txt data.
    --path=<content-path>        Process data from a single path. multiple docs or single docs

                Example: lispat analytics --path=<content-path> --train --array --df

  Comparisons:
    compare                      Compare a standard with a submission

    Args:
    --standard=<content-path>    A standard document to use for comparing against a submission
    --submission=<content-path>  A submission document to use for comparing against a standard.

                Example: lispat compare --standard=<content-path> --submission=<content_path>

  Utilities:
     clean                        remove data in local storage.
     --all                        remove all data in local storage.

"""

import sys
import nltk
import docopt
from lispat.base.manager import CommandManager
from lispat.utils.logger import Logger
from lispat.utils.colors import bcolors


logger = Logger("Main")
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')


def main():

    try:
        args = docopt.docopt(__doc__)
        manager = CommandManager()
        if args['analytics'] and args['--path']:
            user_path = args['--path']
            manager.create_path(user_path)
            manager.run_analytics(args)

        if args['compare'] and args['--standard'] and args['--submission']:
            std_path = args['--standard']
            sub_path = args['--submission']

            manager.create_path(std_path, sub_path)

            manager.run_sub_vs_std(args)
        if args['compare'] and args['input'] and args['--standard']:
            print(args['--text'])
            std_path = args['--standard']
            print(std_path)
            manager.create_path(std_path)
            manager.run_sub_vs_txt(args)

        if args['clean']:
            manager.clean(args)

    except KeyboardInterrupt:
        logger.getLogger().error(bcolors.FAIL + "Keyboard interrupt. Exiting"
                                 + bcolors.ENDC)
        sys.exit(1)


if __name__ == '__main__':
    main()
